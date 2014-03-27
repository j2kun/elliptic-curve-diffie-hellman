from elliptic import *
from finitefield.finitefield import FiniteField

import os


def generateSecretKey(numBits):
   return int.from_bytes(os.urandom(numBits // 8), byteorder='big')


def sendDH(privateKey, generator, sendFunction):
   return sendFunction(privateKey * generator)


def receiveDH(privateKey, receiveFunction):
   return privateKey * receiveFunction()


def slowOrder(point):
   Q = point
   i = 1
   while True:
      if type(Q) is Ideal:
         return i
      else:
         Q = Q + point
         i += 1


if __name__ == "__main__":
   F = FiniteField(3851, 1)

   # Totally insecure curve: y^2 = x^3 + 324x + 1287
   curve = EllipticCurve(a=F(324), b=F(1287))

   # order is 1964
   basePoint = Point(curve, F(920), F(303))

   aliceSecretKey = generateSecretKey(8)
   bobSecretKey = generateSecretKey(8)

   print('Secret keys are %d, %d' % (aliceSecretKey, bobSecretKey))

   alicePublicKey = sendDH(aliceSecretKey, basePoint, lambda x:x)
   bobPublicKey = sendDH(bobSecretKey, basePoint, lambda x:x)

   sharedSecret1 = receiveDH(bobSecretKey, lambda: alicePublicKey)
   sharedSecret2 = receiveDH(aliceSecretKey, lambda: bobPublicKey)
   print('Shared secret is %s == %s' % (sharedSecret1, sharedSecret2))

   print('extracing x-coordinate to get an integer shared secret: %d' % (sharedSecret1.x.n))

