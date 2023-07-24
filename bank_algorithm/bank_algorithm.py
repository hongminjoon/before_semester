# 패키지/모듈 선언
import pickle
from random import *


# 클래스 선언
class Create_User: # User 생성 클래스
    def __init__(self):
        self.input_chance = 2
        self.initial_amount = '100000'
        self.overlap = False
        try:
            print(' ')
            print('----------------현재 유저 정보----------------')
            print('format. 이름, 아이디, 비밀번호, 계좌번호, 잔액')
            with open('User.txt','r',encoding='utf8') as self.User:
                while True:
                    line = (self.User.readline()).strip('\n')
                    if not line: break
                    print(line)
            print('-------------------------------------------')
        except: # 유저가 1명도 없을 경우
            print('현재 존재하는 User가 없습니다.')
            pass

    def CreateIDPW(self):
        User_name = input('User 생성 기능입니다.\n이름을 입력해주십시요.\n : ')
        if User_name == 'Exit':
            return '0'
        
        # User_Data 초기화
        User_Data = ''

        # User_Data에 User_name 추가
        User_Data += User_name + ','

        ID=input('아이디를 입력해주십시요. (단, 영어 및 숫자 조합과 최소 4자리 이상 기입)\n : ')
        if ID == 'Exit':
            return '0'
        
        # 읽어 들여서 같은 ID 기존에 있으면=True
        try:
            with open('User.txt','r',encoding='utf8') as self.User:
                while True:
                    line = self.User.readline()
                    line = line.split(',')
                    if line[1].strip('\n') == ID: # 개행문자 제거
                        self.overlap = True
                    else:
                        if not line: break
                        else: pass
        except: # 유저가 1명도 없을 경우 pass
            pass
        
        while len(ID) < 4 or \
            ((any(char.isalpha() for char in ID)) and (any(char.isdigit() for char in ID)) == False) or \
            self.overlap == True:

            if len(ID) < 4:
                ID = input('4자리 미만으로 입력하셨습니다.\n아이디를 다시 입력해주십시요.\n : ')
                if ID == 'Exit':
                    return '0'
                self.input_chance -= 1

            elif (any(char.isalpha() for char in ID)) and (any(char.isdigit() for char in ID)) == False: # 한글이면?
                ID = input('영어 및 숫자 조합으로 입력해주십시요. \n아이디를 다시 입력해주십시요.\n : ')
                if ID == 'Exit':
                    return '0'
                self.input_chance -= 1

            elif self.overlap == True:
                ID = input('입력하신 아이디가 기존에 존재합니다.\n아이디를 다시 입력해주십시요.\n : ')
                if ID == 'Exit':
                    return '0'
                self.input_chance -= 1
                self.overlap = False

            if self.input_chance == 0: 
                print('3회 이상 오입력 하셨습니다. 해당기능 종료합니다.')
                self.input_chance = 2
                return '0'
        
        # self.input_chance 초기화
        self.input_chance = 2

        # User_Data에 ID 정보 추가
        User_Data += ID + ','

        PW=input('비밀번호를 입력해주십시요. (단, 대문자 1개 필수, 문자, 숫자 및 특수문자 조합하여 기입)\n : ')
        if PW == 'Exit':
            return '0'
        
        while len(PW)<8 or \
            (any(char.isalpha() for char in PW) == False) or \
            (any(char.isdigit() for char in PW) == False) or \
            (any(char.isupper() for char in PW) == False) or \
            PW.isalnum() == True:

            if len(PW) < 8:
                PW = input('8자리 미만으로 입력하셨습니다.\n비밀번호를 다시 입력해주십시요.\n : ')
                if PW == 'Exit':
                    return '0'
                self.input_chance -= 1

            elif any(char.isalpha() for char in PW) == False:
                PW = input('패스워드에 문자가 없습니다. \n비밀번호를 다시 입력해주십시요.\n : ')
                if PW == 'Exit':
                    return '0'
                self.input_chance -= 1

            elif any(char.isdigit() for char in PW) == False:
                PW = input('패스워드에 숫자가 없습니다. \n비밀번호를 다시 입력해주십시요.\n : ')
                if PW == 'Exit':
                    return '0'
                self.input_chance -= 1

            elif any(char.isupper() for char in PW) == False:
                PW = input('패스워드에 대문자가 없습니다. \n비밀번호를 다시 입력해주십시요.\n : ')
                if PW == 'Exit':
                    return '0'
                self.input_chance -= 1

            elif PW.isalnum() == True:
                PW = input('패스워드에 특수문자가 없습니다. \n비밀번호를 다시 입력해주십시요.\n : ')
                if PW == 'Exit':
                    return '0'
                self.input_chance -= 1

            if self.input_chance == 0:
                print('3회 이상 오입력 하셨습니다. 해당기능 종료합니다.')
                self.input_chance = 3
                return '0'
        while True:
            PW_re = input('입력하신 비밀번호를 확인하기 위해 다시 입력해주십시요.\n : ')
            if PW_re == 'Exit':
                return '0'
            if PW == PW_re:
                break
        
        # self.input_chance 초기화
        self.input_chance = 2

        # User_Data에 ID 정보 추가
        User_Data += PW + ','
        
        # 임시 계좌번호 생성 ( 랜덤 숫자 8 자리로 구성 )
        account_number = ''
        for i in range(8): account_number += str(randrange(0,10))

        # 임시 계좌번호와 같은 계좌번호 있는지 확인
        try:
            with open('User.txt','r',encoding='utf8') as self.User:
                while True:
                    line = self.User.readline()
                    line = line.split(',')
                    if line[3].strip('\n') == account_number: # 개행문자 제거
                        for i in range(8): account_number += str(randrange(0,10))
                    else:
                        if not line: break
                        else: pass
        except: # 유저가 1명도 없을 경우 pass
            pass

        # User_Data에 계좌번호와 초기 금액 정보 추가
        User_Data += account_number + ',' + self.initial_amount

        try: # 첫 유저이면 개행문자 없이 추가
            with open('User.txt','r',encoding = 'utf8') as self.User:
                pass
            with open('User.txt','a',encoding = 'utf8') as self.User:
                self.User.write('\n'+User_Data)
        except:
            with open('User.txt','a',encoding = 'utf8') as self.User:
                self.User.write(User_Data)
        return '0'
            
class Print_User: # 모든 User의 상태를 출력하는 클래스
    def __init__(self):
        try:
            print(' ')
            print('----------------현재 유저 정보----------------')
            print('format. 이름, 아이디, 비밀번호, 계좌번호, 잔액')
            with open('User.txt','r',encoding='utf8') as self.User:
                while True:
                    line = (self.User.readline()).strip('\n')
                    if not line: break
                    print(line)
            print('-------------------------------------------\n')
        except: # 유저가 1명도 없을 경우
            print('현재 존재하는 User가 없습니다.')

class Send_Money: # 랜덤 User에게 송금하는 클래스
    def __init__(self):
        pass
    
    def send_money(self):    
        # 총 유저 수 초기화
        User_number = -1

        # 총 유저 수 구하기
        with open('User.txt','r',encoding='utf8') as self.User:
            while True:
                line = self.User.readline()
                User_number += 1
                if not line: break

        for i in range(randint(User_number, User_number+10)): # 최소 유저수 만큼 진행

            self.amount = input('송금할 금액을 입력해주십시요.\n : ')
            if self.amount == 'Exit':
                return '0'
            
            S_num = randint(1, User_number) # random 송금자 위치 설정
 
            # User.txt 에서 송금자의 S_line (Sender_line) 저장
            with open('User.txt','r',encoding='utf8') as self.User:
                for i in range(S_num):
                    S_line = self.User.readline()
                    S_line = S_line.split(',')
            
            # 송금자 잔액 정보 New_S_balance
            Old_S_line = S_line # 삭제할 송금자 정보
            New_S_balance = str(int(Old_S_line[4]) - int(self.amount))

            # 이채 시 잔액이 부족한 경우
            if int(New_S_balance) < 0:
                print(f'{Old_S_line[0]}님의 잔액이 {abs(int(New_S_balance))}만큼 부족합니다. 초기화면으로 돌아갑니다.')
                return '0'
            
            # 송금자의 Old_line 을 삭제
            with open('User.txt','r',encoding='utf8') as self.User:
                lines = self.User.readlines()
            with open('User.txt','w',encoding='utf8') as self.User:
                for line in lines:
                    if line.strip('\n') != (','.join(Old_S_line)).strip('\n') :
                        self.User.write(line)
            
            # 송금자 New 정보 선언 (New_S_line)
            New_S_line = Old_S_line
            New_S_line[4] = New_S_balance

            # 송금자 New 정보를 입력
            if S_num == User_number: # 송금자가 마지막 위치에 있으면 Old_S_line 삭제 후 빈 한 줄이 남는 것을 처리
                with open('User.txt','a',encoding='utf8') as self.User:
                    self.User.write(','.join(New_S_line))
            else:
                with open('User.txt','a',encoding='utf8') as self.User:
                    self.User.write('\n' + ','.join(New_S_line))

            # 송금자와 수금자가 같지 않게 처리.
            while True:
                R_num = randint(1,User_number)
                if R_num != User_number:
                    break

            # User.txt 에서 수금자의 R_line (Receiver_line) 저장
            with open('User.txt','r',encoding='utf8') as self.User:
                for i in range(R_num):
                    R_line = self.User.readline()
                    R_line = R_line.split(',')
            
            # 수금자 New 정보 : 잔액에 self.amount 만큼 추가한 정보
            Old_R_line = R_line
            New_R_Balance = str(int(Old_R_line[4]) + int(self.amount))

            # 수금자 old 정보 삭제
            with open('User.txt','r',encoding='utf8') as self.User:
                lines = self.User.readlines()
            with open('User.txt','w',encoding='utf8') as self.User:
                for line in lines:
                    if line.strip('\n') != (','.join(Old_R_line)).strip('\n') :
                        self.User.write(line)


            # 수금자 New 정보 선언 (New_R_line)
            New_R_line = Old_R_line
            New_R_line[4] = New_R_Balance

            # 수금자 New 정보를 입력
            with open('User.txt','a',encoding='utf8') as self.User:
                self.User.write('\n' + ','.join(New_R_line))

            # 유저의 이름으로 계좌 송금 기록을 따로 보관
            try:
                with open(New_S_line[0]+'.txt','r',encoding='utf8') as self.User:
                    self.User.readline()
                with open(New_S_line[0]+'.txt','a',encoding='utf8') as self.User:
                    self.User.write(f'\n**출금 ( {New_R_line[0]} 님에게 ) : {self.amount}원**\n ===> 현재 잔액 : {New_S_line[4]}원\n')
            except:
                with open(New_S_line[0]+'.txt','w',encoding='utf8') as self.User:
                    self.User.write(f'**출금 ( {New_R_line[0]} 님에게 ) : {self.amount}원**\n ===> 현재 잔액 : {New_S_line[4]}원\n')

            # 유저의 이름으로 계좌 입금 기록을 따로 보관
            try:
                with open(New_R_line[0]+'.txt','r',encoding='utf8') as self.User:
                    self.User.readline()
                with open(New_R_line[0]+'.txt','a',encoding='utf8') as self.User:
                    self.User.write(f'\n**입금 ( {New_S_line[0]} 님으로부터 ) : {self.amount}원**\n ===> 현재 잔액 : {New_R_line[4]}원\n')
            except:
                with open(New_R_line[0]+'.txt','w',encoding='utf8') as self.User:
                    self.User.write(f'**입금 ( {New_S_line[0]} 님으로부터 ) : {self.amount}원**\n ===> 현재 잔액 : {New_R_line[4]}원\n')
        
        return '0'

class User_Delete: # 선택한 User 삭제하는 클래스
    def __init__(self):
        pass

    def user_delete(self):
        self.input_chance = 3

        Delete_ID = input('유저 삭제 서비스 입니다. 삭제하실 유저의 아이디를 입력해주십시요.\n : ')
        if Delete_ID == 'Exit':
            return '0'

        with open('User.txt', 'r', encoding='utf8') as self.User:
            while True:
                line = self.User.readline()
                line = line.split(',')
                if line[1].strip('\n') == Delete_ID:
                    break
        
        # 삭제할 유저 정보
        Delete_line = line

        while True:
            if self.input_chance == 0:
                print('\n3회 이상 오입력 하셨습니다. 해당기능 종료합니다.')
                return '0'

            Delete_PW = input('삭제하실 유저의 비밀번호를 입력해주십시요.\n : ')
            if Delete_PW == 'Exit':
                return None
            
            if Delete_PW == Delete_line[2].strip('\n'): # 입력한 패스워드가 맞다면,

                # 해당되는 유저 삭제
                with open('User.txt','r',encoding='utf8') as self.User:
                        lines = self.User.readlines()
                with open('User.txt','w',encoding='utf8') as self.User:
                    for line in lines:
                        if line.strip('\n') != (','.join(Delete_line)).strip('\n') :
                            self.User.write(line)
                
                print('입력하신 User가 삭제되었습니다.')
                break

            else:
                print('\n비밀번호를 잘못 입력하셨습니다. 다시 입력해주세요.')
                self.input_chance -= 1
                pass
        return '0'


# 첫 서비스 입력
service_no = input('은행 서비스 프로그램 입니다.\
            \n제공되는 서비스를 안내해드리겠습니다. 안내에 맞게 원하시는 서비스를 입력해주십시요.\
            \n1번 서비스 [1 입력] : User 생성 ( 이름, ID, Password, 계좌번호 )\
            \n2번 서비스 [2 입력] : 모든 User의 상태 출력\
            \n3번 서비스 [3 입력] : 랜덤 User에게 송금\
            \n4번 서비스 [4 입력] : User 삭제\
            \n마지막으로, 모든 어플리케이션에서 Exit를 입력 시 되돌아 가며, 초기에 입력 시에는 프로그램이 종료됩니다. 감사합니다.\
            \n서비스 입력란 : ')

if service_no == 'Exit': # 첫 입력에 'Exit' 입력 시
    exit()

while True:
    if service_no == '1':
        call = Create_User()
        if call.CreateIDPW() == '0':
            service_no = '0'

    if service_no == '2':
        Print_User()
        service_no = '0'
    
    if service_no == '3':
        call = Send_Money()
        if call.send_money() == '0':
            service_no = '0'
    
    if service_no == '4':
        call = User_Delete()
        if  call.user_delete() == '0':
            service_no = '0'
    
    if service_no != '0' and '1' and '2' and '3' and '4':
        print('\n***********************************')
        print('잘못된 값을 입력하셨습니다.')
        print('1, 2, 3, 4 중에 한가지를 입력해주십시요.')
        print('***********************************')
        service_no = '0'

    if service_no == '0':
        service_no = input('\n은행 서비스 프로그램 입니다.\
            \n제공되는 서비스를 안내해드리겠습니다. 안내에 맞게 원하시는 서비스를 입력해주십시요.\
            \n1번 서비스 [1 입력] : User 생성 ( ID, Password, 계좌번호 )\
            \n2번 서비스 [2 입력] : 모든 User의 상태 출력\
            \n3번 서비스 [3 입력] : 랜덤 User에게 송금\
            \n4번 서비스 [4 입력] : User 삭제\
            \n마지막으로, 모든 어플리케이션에서 Exit를 입력 시 되돌아 가며, 초기에 입력 시에는 프로그램이 종료됩니다. 감사합니다.\
            \n서비스 입력란 : ')
        if service_no == 'Exit':
            print('\n프로그램을 종료합니다. 감사합니다.')
            break