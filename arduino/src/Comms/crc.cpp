#include <iostream>
#include <cmath>
#include "crc.h"


int binLen(int num) {
    int len = 0;
    for (int i = 0; i < 1024; i++) {
        if (num != 0) {
            len++;
        } else {
            return len;
        }
        num = num >> 1;
    }
    return 0;
}

void binPrint(int num) {
    int len = binLen(num);
    int buf[len];
    for (int i = 0; i < len; i++) {
        buf[(len-i)-1] = num % 2;
        num = num >> 1;
    }
    for (auto c : buf) {
        std::cout << c;
    }
    std::cout << std::endl;
}

int calcCRC(int message) {
    // add n empty bits to the left
    message <<= POLYNOM_LEN;
    int rem = message;
    do {
        int shift = binLen(rem)-binLen(POLYNOMIAL);
        int temp = POLYNOMIAL << shift;
        binPrint(rem);
        binPrint(temp);
        std::cout << std::endl;
        rem = rem ^ temp;
    } while (binLen(rem) > POLYNOM_LEN);
    binPrint(rem);
    return rem;
}

int main() {
    int msg = 0b11110110110;
    int rem = calcCRC(msg);
    msg <<= (POLYNOM_LEN-1);
    binPrint(msg+rem);
    calcCRC(msg + rem);
    return 0;
}