class IAS:
    def __init__(self, Memory):
        self.Memory = Memory
        self.PC = '{0:010b}'.format(0)
        self.AC = '{0:040b}'.format(0)
        self.IR = '{0:08b}'.format(0)
        self.MAR = '{0:012b}'.format(0)
        self.MBR = '{0:040b}'.format(0)
        self.IBR = '{0:020b}'.format(0)
        self.MQ = '{0:040b}'.format(0)
        self.instructions = {

            # Start of Data Transfer Instructions

            # LOAD MQ Transfer contents of register MQ to the accumulator AC
            '00001010': self.LOAD_MQ,
            # LOAD MQ,M(X) Transfer contents of memory location X to MQ
            '00001001': self.LOAD_MQ_MX,
            # STOR M(X) Transfer contents of accumulator to memory location X
            '00100001': self.STOR_MX,
            # LOAD M(X) Transfer M(X) to the accumulator
            '00000001': self.LOAD_MX,
            # LOAD -M(X) Transfer -M(X) to the accumulator
            '00000010': self.LOAD_notMX,
            # LOAD |M(X)| Transfer absolute value of M(X) to the accumulator
            '00000011': self.LOAD_modMX,
            # LOAD -|M(X)| Transfer -|M(X)| to the accumulator
            '00000100': self.LOAD_notmodMX,

            # End of Data Transfer Instructions

            # Start of Unconditional Branch Instructions

            # JUMP M(X,0:19) Take next instruction from left half of M(X)
            '00001101': self.JUMP_MX_LHS,
            # JUMP M(X,20:39) Take next instruction from right half of M(X)
            '00001110': self.JUMP_MX_RHS,

            # End of Unconditional Branch Instructions

            # Start of Conditional Branch Instructions

            # JUMP+M(X,0:19) If number in the accumulator is nonnegative, take next instruction from left half of M(X)
            '00001111': self.JUMP_IF_MX_LHS,

            # JUMP+M(X,20:39) If number in the accumulator is nonnegative , take next instruction from right half of M(X)
            '00010000': self.JUMP_IF_MX_RHS,

            # End of Conditional Branch Instructions

            # Start of Arithmetic Instructions

            # ADD M(X) Add M(X) to AC; put the result in AC
            '00000101': self.ADD_MX,
            # ADD |M(X)| Add |M(X)| to AC; put the result in AC
            '00000111': self.ADD_modMX,
            # SUB M(X) Subtract M(X) from AC; put the result in AC
            '00000110': self.SUB_MX,
            # SUB |M(X)| Subtract |M(X)| from AC; put the remainder in AC
            '00001000': self.SUB_modMX,
            # MUL M(X) Multiply M(X) by MQ; put most significant bits of result in AC, put less significant bits in MQ
            '00001011': self.MUL_MX,
            # DIV M(X) Divide AC by M(X); put the quotient in MQ and the remainder in AC
            '00001100': self.DIV_MX,
            # LSH Multiply accumulator by 2; i.e., shift left one bit position
            '00010100': self.LSH,
            # RSH Divide accumulator by 2; i.e., shift right one bit position
            '00010101': self.RSH,

            # End of Arithmetic Instructions

            # Start of Address Modify Instructions

            # STOR M(X,8:19) Replace left address field at M(X) by 12 rightmost bits of AC
            '00010010': self.STOR_MX_LHS,
            # STOR M(X,28:39) Replace right address field at M(X) by 12 rightmost bits of AC
            '00010011': self.STOR_MX_RHS,

            # End of Address Modify Instructions
        }

    def LOAD_MQ(self):
        self.AC = self.MQ

    def LOAD_MQ_MX(self):
        self.MBR = self.Memory[int(self.MAR, 2)]
        self.MQ = self.MBR

    def LOAD_MX(self):
        self.MBR = self.Memory[int(self.MAR, 2)]
        self.AC = self.MBR

    def LOAD_notMX(self):
        self.MBR = self.Memory[int(self.MAR, 2)]
        self.AC = str(1 - int(MBR[0], 2)) + MBR[1:]

    def LOAD_modMX(self):
        self.MBR = self.Memory[int(self.MAR, 2)]
        self.AC = '0' + MBR[1:]

    def LOAD_notmodMX(self):
        self.MBR = self.Memory[int(self.MAR, 2)]
        self.AC = '1' + MBR[1:]

    def STOR_MX(self):
        self.MBR = self.AC
        self.Memory[int(self.MAR, 2)] = self.MBR

    def ADD_MX(self):
        self.MBR = self.Memory[int(self.MAR, 2)]
        val = int(self.AC[1:], 2)*(pow(-1, int(self.AC[0]))) + \
            int(self.MBR[1:], 2)*(pow(-1, int(self.MBR[0], 2)))
        if(val < 0):
            self.AC = '1' + '{0:039b}'.format(-val)
        else:
            self.AC = '{0:040b}'.format(val)

    def ADD_modMX(self):
        self.MBR = self.Memory[int(self.MAR, 2)]
        val = int(self.AC[1:], 2) * \
            (pow(-1, int(self.AC[0]))) + int(str(self.MBR[1:], 2))
        if(val < 0):
            self.AC = '1' + '{0:039b}'.format(-val)
        else:
            self.AC = '{0:040b}'.format(val)

    def SUB_MX(self):
        self.MBR = self.Memory[int(self.MAR, 2)]
        a = int(self.AC[1:], 2)*(pow(-1, int(self.AC[0], 2)))
        b = int(self.MBR[1:], 2)*(pow(-1, int(self.MBR[0], 2)))

        val = a-b
        if(val < 0):
            self.AC = '1' + '{0:039b}'.format(-val)
        else:
            self.AC = '{0:040b}'.format(val)

    def SUB_modMX(self):
        self.MBR = self.Memory[int(self.MAR, 2)]
        val = int(self.AC[1:], 2) * \
            (pow(-1, int(self.AC[0]))) - int(self.MBR[1:], 2)
        self.AC = '{0:040b}'.format(val)
        if(val < 0):
            self.AC = '1' + '{0:039b}'.format(-val)
        else:
            self.AC = '{0:040b}'.format(val)

    def MUL_MX(self):
        self.MBR = self.Memory[int(self.MAR, 2)][1:]
        a = int(self.MBR[1:], 2)*(pow(-1, int(self.MBR[0])))
        b = int(self.MQ[1:], 2)*(pow(-1, int(self.MQ[0])))
        val = a*b
        bval = ""
        if(val < 0):
            bval = '1' + '{0:039b}'.format(-val)
        else:
            bval = '{0:040b}'.format(val)
        self.AC = bval[:40]
        if len(bval) > 40:
            self.MQ = '{0:040b}'.format(int(bval[40:], 2))

    def DIV_MX(self):
        self.MBR = self.Memory[int(self.MAR, 2)]
        a = int(self.MBR[1:], 2)*(pow(-1, int(self.MBR[0])))
        b = int(self.AC[1:], 2)*(pow(-1, int(self.AC[0])))
        quotient = b//a
        remainder = b % a
        if(quotient < 0):
            self.MQ = '1' + '{0:039b}'.format(-quotient)
        else:
            self.MQ = '{0:040b}'.format(quotient)
        if(remainder < 0):
            self.AC = '1' + '{0:039b}'.format(-remainder)
        else:
            self.AC = '{0:040b}'.format(remainder)

    def LSH(self):
        self.AC = self.AC[0] + self.AC[2:40] + '0'

    def RSH(self):
        self.AC = self.AC[0] + '0' + self.AC[1:39]

    def STOR_MX_LHS(self):
        self.MBR = self.AC
        val = self.Memory[int(self.MAR, 2)]
        self.Memory[int(self.MAR, 2)] = val[0:8] + self.MBR[28:40] + val[20:40]

    def STOR_MX_RHS(self):
        self.MBR = self.AC
        val = self.Memory[int(self.MAR, 2)]
        self.Memory[int(self.MAR, 2)] = val[0:28] + self.MBR[28:40]

    def JUMP_MX_LHS(self):
        self.PC = '{0:010b}'.format(int(self.MAR, 2))

    def JUMP_MX_RHS(self):
        self.PC = '{0:010b}'.format(int(self.MAR, 2))
        self.IBR = self.Memory[int(self.MAR, 2)][20:40]

    def JUMP_IF_MX_LHS(self):
        if(int(self.AC[1:], 2)*(int(self.AC[0], 2)*(-1)) >= 0):
            self.PC = '{0:010b}'.format(int(self.MAR, 2))

    def JUMP_IF_MX_RHS(self):
        if(int(self.AC[1:], 2)*(int(self.AC[0], 2)*(-1)) >= 0):
            self.PC = '{0:010b}'.format(int(self.MAR, 2))
            self.IBR = self.Memory[int(self.MAR, 2)][20:40]

    def fetch(self):
        if(int(self.IBR, 2) == 0):
            self.MAR = self.PC
            self.MBR = self.Memory[int(self.MAR, 2)]
            if(int(self.MBR[0:20], 2) == 0):
                self.IR = self.MBR[20:28]
                self.MAR = self.MBR[28:40]
                self.PC = '{0:010b}'.format(int(self.PC, 2) + 1)
            else:
                self.IBR = self.MBR[20:40]
                self.IR = self.MBR[0:8]
                self.MAR = self.MBR[8:20]
        else:
            self.IR = self.IBR[0:8]
            self.MAR = self.IBR[8:20]
            self.IBR = '{0:040b}'.format(0)
            self.PC = '{0:010b}'.format(int(self.PC, 2) + 1)

    def decode(self):
        if(self.IR != '11111111'):
            print('\n***********' +
                  self.instructions[self.IR].__name__ + '***********\n')
            self.instructions[self.IR]()
        else:
            print("\n************HALT***********\n")

    def execute(self):
        while(int(self.PC, 2) < 1000 and self.IR != '11111111'):
            self.fetch()
            self.decode()
            print("PC:  ", self.PC, "PC value: ", int(self.PC, 2))
            print("IR:  ", self.IR)
            print("IBR: ", self.IBR)
            print("MAR: ", self.MAR, "MAR value: ", int(self.MAR, 2))
            print("MBR: ", self.MBR)
            print("AC:  ", self.AC, "AC value: ", int(
                self.AC[1:], 2)*pow(-1, int(self.AC[0])))
            print("MQ:  ", self.MQ, "MQ value: ", int(
                self.MQ[1:], 2)*pow(-1, int(self.MQ[0])))


class Test:
    def __init__(self):
        # Creating 1000 40-bit locations
        self.Memory = ['{0:040b}'.format(0)]*1000

    def Test1(self):
        ''' Random Instructions:
            LOAD M[100] : 00000001 000001100100 DIV M[101] : 00001100 000001100101 0
            ADD M[102]  : 00000101 000001100110 STOR M[103]: 00100001 000001100111 1
            LOAD MQ     : 00001010 000000000000 MUL M[103] : 00001011 000001100111 2
            SUB M[101]  : 00000110 000001100101 RSH        : 00010101 000000000000 3
            LOAD M[105] : 00000001 000001101001 STOR M(7,28:39): 00010011 000000000111 4
                                           JUMP M(7,20:39) : 00001110 000000000111 5
                                                                                   6
                                              STOR M[103]  : 00100001 000001101000 7
            HALT     : 11111111 000000000000                                       8
        '''
        self.Memory[0:8] = [
            '0000000100000110010000001100000001100101',
            '0000010100000110011000100001000001100111',
            '0000101000000000000000001011000001100111',
            '0000011000000110010100010101000000000000',
            '0000000100000110100100010011000000000111',
            '0000000000000000000000001110000000000111',
            '0000000000000000000000000000000000000000',
            '0000000000000000000000100001000001100111',
            '1111111100000000000000000000000000000000',
        ]
        self.Memory[100:106] = [
            '0000000000000000000000000000000000001011',  # 11
            '0000000000000000000000000000000000000011',  # 3
            '0000000000000000000000000000000000001110',   # 14
            '0000000000000000000000000000000000000000',   # 0
            '0000000000000000000000000000000000000000',
            '0000000000000000000000000000000001101000',  # 104
        ]
        print("\nTest 1 of Random Instructions:")
        ias = IAS(self.Memory)
        ias.execute()
        print("\n**********************************\n")
        print("Memory Location 103 val:", self.Memory[103], int(
            self.Memory[103][1:], 2)*pow(-1, int(self.Memory[103][0], 2)))
        print("Memory Location 104 val:", self.Memory[104], int(
            self.Memory[104][1:], 2)*pow(-1, int(self.Memory[104][0], 2)))

        print("**************End of Test 1*****************")

    def Test2(self):
        ''' Given Program:
            main() { 
            int a =14,b=3,c; 
            if(a >=b) 
            c  =  a / b; 
            else 
            c  = a*b;
            } 
            LOAD M[100] , SUB M[101]
                        , JUMP+M(4,0:19)
            LOAD MQ M[100] , MUL M[101]
                          JUMP M(5,0:19)
            LOAD M[100] , DIV M[101]
            STOR M[102]      , HALT
        '''
        self.Memory[0:6] = [
            '0000000100000110010000000110000001100101',
            '0000000000000000000000001111000000000100',
            '0000100100000110010000001011000001100101',
            '0000000000000000000000001101000000000101',
            '0000000100000110010000001100000001100101',
            '0010000100000110011011111111000000000000',
        ]
        self.Memory[100:103] = [
            '0000000000000000000000000000000000001110',  # a = 14
            '0000000000000000000000000000000000000011',  # b = 3
            '0000000000000000000000000000000000000000',  # c = 0
        ]
        print("\nTest 2 of Given Program:")
        ias = IAS(self.Memory)
        ias.execute()
        print("\n**********************************\n")
        print("Memory Location 102 val (c) :", self.Memory[102], int(
            self.Memory[102][1:], 2)*pow(-1, int(self.Memory[102][0], 2)))
        print("\n**************End of Test 2*****************")


test = Test()
test.Test1()
test.Test2()
