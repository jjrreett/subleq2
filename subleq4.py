acs = 1 << 0  # address counter select (o selects pc)
rdb = 1 << 1  # read to bus
ldi = 1 << 2  # load address 0
ldj = 1 << 3  # load address 1
lda = 1 << 4  # load a reg
ldb = 1 << 5  # load b reg
wrt = 1 << 6  # write alu out bus
inc = 1 << 7  # inc program counter
jmp = 1 << 8  # load program counter
rst = 1 << 9  # reset instruction counter


ism = [0] * (1 << 5)


ism[0x0] = rdb + ldi + inc  # load mem[pc] (&A0) into ADDR reg 0 and pc++
ism[0x1] = rdb + ldj  # load mem[pc] (&A1) into ADDR reg 1
ism[0x2] = acs + rdb + lda + inc  # read into A reg (generally mem[&A]) and pc++
ism[0x3] = rdb + ldi + inc  # load mem[pc] (&B0) into ADDR reg 0 and pc++
ism[0x4] = rdb + ldj  # load mem[pc] (&B1) into ADDR reg 1
ism[0x5] = acs + rdb + ldb  # read into B reg (generally mem[&B]) and pc++
ism[0x6] = acs + wrt + inc  # write alu to bus, (generally mem[&B]) and pc++
# if leq0=0
ism[0x7] = inc  # pc++
ism[0x8] = inc + rst  # pc++ and reset inst counter
# if leq0=1
ism[0x17] = rdb + ldi + inc  # load mem[pc] (&C) into pc and reset inctruction counter
ism[0x18] = rdb + ldj  # load mem[pc] (&C) into pc and reset inctruction counter
ism[0x19] = jmp + rst  # load mem[pc] (&C) into pc and reset inctruction counter

ism[0x10] = ism[0x0]
ism[0x11] = ism[0x1]
ism[0x12] = ism[0x2]
ism[0x13] = ism[0x3]
ism[0x14] = ism[0x4]
ism[0x15] = ism[0x5]
ism[0x16] = ism[0x6]

for i, instruction in enumerate(ism):
    print(f"{i:#04x}: {instruction: #06x}")

"""
0x00   0x01   0x02   0x04   0x08   0x10   0x20   0x40   0x80   0x100   
       EMEM + LDRG                                                 
SADR + EMEM        + LARG               + IPRC              
       EMEM + LDRG                                                 
SADR + EMEM               + LBRG                                   
SADR +                             LDOM + IPRC              
                                          IPRC        + RISC
       EMEM                                    + LPRC + RISC        
"""

data = [0] * (1 << 15)

inp = 0xE000
out = 0xE001
stop = 0xFFFF
z = 0x0100
a = 0x0101
b = 0x0102
dat = [
    inp,
    z,
    6,
    z,
    a,
    12,
    z,
    z,
    18,
    inp,
    z,
    24,
    z,
    b,
    30,
    z,
    z,
    36,
    a,
    z,
    42,
    b,
    z,
    48,
    z,
    out,
    52,
    z,
    z,
    stop,
]

for i, d in enumerate(dat):
    data[i] = d

ddata = []
for d in data:
    ddata.extend(
        (
            0xFF & d,
            (0xFF00 & d) >> 8,
        )
    )

for i in range(0, 60, 6):
    try:
        print(
            f"{i:04x}: {ddata[i]:02x} {ddata[i+1]:02x} {ddata[i+2]:02x} {ddata[i+3]:02x} {ddata[i+4]:02x} {ddata[i+5]:02x}"
        )
    except IndexError:
        break
print()
# for i in range(0, 60, 6):
#     d = ddata[i]
#     print(f"{i:04x}: {d:02x}", end="")
#     print(f": {bytes(d)}")


with open("mem", "wb") as file:
    file.write(bytes(ddata))
