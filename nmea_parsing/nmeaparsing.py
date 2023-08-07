import serial
import pyproj
import pandas as pd

from parsing_interface.msg import Parsing
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSHistoryPolicy
from rclpy.qos import QoSProfile
from rclpy.qos import QoSReliabilityPolicy


class NMEA_Parsing:
    def __init__(self, PORT, BaudRate):
        self.PORT = PORT
        self.BaudRate = BaudRate

    def parsing(self, Message_ID):
        self.ser = serial.Serial(self.PORT, self.BaudRate)
        while True:
            if self.ser.readable():
                DATA = self.ser.readline()
                DATA = DATA.decode(encoding='utf8', errors='ignore')[0:len(DATA) - 1]
                DATA_split = DATA.split(',')
                if DATA[1:6] == Message_ID and len(DATA_split) == 15 and len(DATA) >= 70:
                    self.DATA = DATA.strip()
                    self.DATA_split = self.DATA.split(',')
                    self.lat, self.lon = self.DATA_split[2], self.DATA_split[4]
                    break

    def Unit_Conversion(self):
        self.WGS84_lat = str(float(self.lat[:2]) + float(self.lat[2:]) / 60)
        self.WGS84_lon = str(float(self.lon[:3]) + float(self.lon[3:]) / 60)

class Projection(NMEA_Parsing):
    def __init__(self, PORT, BaudRate, Message_ID, epsg1, epsg2):
        NMEA_Parsing.__init__(self, PORT, BaudRate)
        NMEA_Parsing.parsing(self, Message_ID)
        NMEA_Parsing.Unit_Conversion(self)
        self.epsg1 = epsg1
        self.epsg2 = epsg2

    def projetction(self):
        self.proj1 = pyproj.CRS(self.epsg1)
        self.proj2 = pyproj.CRS(self.epsg2)
        self.transformer = pyproj.Transformer.from_crs(self.proj1, self.proj2)

    def convert_coordinates(self):
        self.new_lat, self.new_lon = self.transformer.transform(self.WGS84_lat, self.WGS84_lon)
        self.new_lat , self.new_lon = str(self.new_lat) , str(self.new_lon)

class NMEAParsing(Node, Projection):
    def __init__(self):
        Node.__init__(self,'nmeaparsing')
        self.declare_parameters(
            namespace='',
            parameters=[
                ('port', '/dev/ttyUSB0'),  # Set default port here
                ('baud_rate', 115200),       # Set default baud rate here
                ('message_id', 'GNGGA'),   # Set default message ID here
                ('epsg1', 'epsg:4326'),    # Set default EPSG1 code here
                ('epsg2', 'epsg:32652')     # Set default EPSG2 code here
            ]
        )
        
        self.port = self.get_parameter('port').get_parameter_value().string_value
        self.baud_rate = self.get_parameter('baud_rate').get_parameter_value().integer_value
        self.message_id = self.get_parameter('message_id').get_parameter_value().string_value
        self.epsg1 = self.get_parameter('epsg1').get_parameter_value().string_value
        self.epsg2 = self.get_parameter('epsg2').get_parameter_value().string_value

        QOS_RKL10V = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=30,
            durability=QoSDurabilityPolicy.VOLATILE)
        
        self.nmea_parsing_publisher = self.create_publisher(
            Parsing,
            'nmea_parsing',
            QOS_RKL10V)

        self.timer = self.create_timer(1.0, self.publish_nmeaparsing)
    
    def publish_nmeaparsing(self):
        
        Projection.__init__(self, self.port, self.baud_rate, self.message_id, self.epsg1, self.epsg2)
        Projection.projetction(self)
        Projection.convert_coordinates(self)
        
        msg = Parsing()
        msg.stamp = self.get_clock().now().to_msg()
        msg.gga_raw_data = self.DATA
        msg.gga_message_id = self.DATA_split[0][1:]
        msg.gga_utc = self.DATA_split[1]
        msg.gga_lat = float(self.WGS84_lat)
        msg.gga_lat_dir = self.DATA_split[3]
        msg.gga_lon = float(self.WGS84_lon)
        msg.gga_lon_dir = self.DATA_split[5]
        msg.gga_quality = int(self.DATA_split[6])
        msg.gga_num_satellite = int(self.DATA_split[7])
        msg.gga_hdop = float(self.DATA_split[8])
        msg.gga_alt = float(self.DATA_split[9])
        msg.gga_alt_unit = self.DATA_split[10]
        msg.gga_sep = float(self.DATA_split[11])
        msg.gga_sep_unit = self.DATA_split[12]
        msg.gga_diff_age = self.DATA_split[13]
        msg.gga_diff_station = self.DATA_split[13]
        msg.gga_check_sum = self.DATA_split[14][len(self.DATA_split[14])-3:]
        msg.gga_utm_lat = float(self.new_lat)
        msg.gga_utm_lon = float(self.new_lon)
    
        try: # csv 파일에 utm 좌표 기록
            df = pd.read_csv('/home/vilab/ros2_ws/coordinates.csv', sep=',',
                    encoding='cp949')  
            data = {'UTM_lat' : float(self.new_lat), 'UTM_lon' : float(self.new_lon)}
            df = pd.concat([df, pd.DataFrame(data, index=[0])], ignore_index=True)
            df.to_csv('/home/vilab/ros2_ws/coordinates.csv', index=False, encoding='cp949')
        
        except: # csv 파일이 없다면, 만들고 기록 
            data_col = ["UTM_lat", "UTM_lon"]
            data = {"UTM_lat": [], "UTM_lon": []}
            user_df = pd.DataFrame(data, columns=data_col)
            user_df.to_csv('/home/vilab/ros2_ws/coordinates.csv',
                        index=False, encoding='cp949')
            
            df = pd.read_csv('/home/vilab/ros2_ws/coordinates.csv', sep=',',
                    encoding='cp949')  
            data = {'UTM_lat' : float(self.new_lat), 'UTM_lon' : float(self.new_lon)}
            df = pd.concat([df, pd.DataFrame(data, index=[0])], ignore_index=True)
            df.to_csv('/home/vilab/ros2_ws/coordinates.csv', index=False, encoding='cp949')


        self.nmea_parsing_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    nmeaparsing = NMEAParsing()
    try:
        try:
            rclpy.spin(nmeaparsing)
        except KeyboardInterrupt:
            nmeaparsing.get_logger().info('Keyboard Interrupt (SIGINT)')
        finally:
            nmeaparsing.destroy_node()
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()

