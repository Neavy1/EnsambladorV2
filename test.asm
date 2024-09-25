main:
        addi    sp, sp, -32
        sw      ra, 28(sp) 
        sw      s0, 24(sp)          
        addi    s0, sp, 32
        mv      a0, zero
        sw      a0, -12(s0)
        addi    a1, zero, 19
        sw      a1, -16(s0)
        addi    a1, zero, 25
        sw      a1, -20(s0)
        sw      a0, -24(s0)
        lw      a1, -16(s0)
        lw      a0, -20(s0)
        bge     a0, a1, LBB0_5
        j       LBB0_1
LBB0_1:
        lw      a0, -20(s0)
        addi    a1, zero, 44
        blt     a0, a1, LBB0_3
        j       LBB0_2
LBB0_2:
        addi    a0, zero, 42
        sw      a0, -24(s0)
        j       LBB0_4
LBB0_3:
        lw      a0, -16(s0)
        sw      a0, -24(s0)
        j       LBB0_4
LBB0_4:
        j       LBB0_6
LBB0_5:
        lw      a0, -20(s0)
        sw      a0, -24(s0)
        j       LBB0_6
LBB0_6:
        mv      a0, zero
        lw      s0, 24(sp)
        lw      ra, 28(sp)
        addi    sp, sp, 32
        ret