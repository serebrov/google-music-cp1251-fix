# -*- coding: UTF-8 -*-

testline = "строка с русскими символами и english letters"
print testline.decode('utf-8')
print testline.decode('utf-8').encode('cp1251')
print testline