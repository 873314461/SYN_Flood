#coding:utf-8
from Tkinter import *
import tkMessageBox
import time
import threading
import json
from send_packet import sendData
class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()
		self.lockSend = threading.Lock()
		self.bSend = False

	def createWidgets(self):
		self.LabIP = Label(self, text = "IP地址", font = ("微软雅黑", 16, "bold"))
		self.LabIP.grid(row = 0, column = 0)
		self.strIP = StringVar()
		self.EntryIP = Entry(self, textvariable = self.strIP, font = ("微软雅黑", 16, "bold"))
		self.EntryIP.grid(row = 0, column = 1)

		self.LabPort = Label(self, text = "端口", font = ("微软雅黑", 16, "bold"))
		self.LabPort.grid(row = 1, column = 0)
		self.strPort = StringVar()
		self.EntryPort = Entry(self, textvariable = self.strPort, font = ("微软雅黑", 16, "bold"))
		self.EntryPort.grid(row = 1, column = 1)

		#开始 结束 按钮
		self.btnStart = Button(self, text = '开 始', command = self.start, font=("微软雅黑", 16, "bold"))
		self.btnStart.grid(row = 8, column = 0)

		self.btnEnd = Button(self, text = '停 止', command = self.end, state = DISABLED, font=("微软雅黑", 16, "bold"))
		self.btnEnd.grid(row = 8, column = 1)
		
	def start(self):
		#更改按钮状态
		self.btnEnd['state'] = ACTIVE
		self.btnStart['state'] = DISABLED
		self.EntryIP['state'] = 'readonly'
		self.EntryPort['state'] = 'readonly'

		self.dst_ip = self.strIP.get()
		self.dst_port = int(self.strPort.get())

		#创建新的进程及信号量
		self.tSendPacket1 = threading.Thread(target=self.do, name="SendPacket-1")
		self.tSendPacket2 = threading.Thread(target=self.do, name="SendPacket-2")

		#修改进程运行标志
		self.lockSend.acquire()
		self.bSend = True
		self.lockSend.release()

		#执行监听进程
		self.tSendPacket1.start()
		self.tSendPacket2.start()

	def end(self):
		#修改进程运行标志
		self.lockSend.acquire()
		self.bSend = False
		self.lockSend.release()

		#修改按钮状态
		self.btnEnd['state'] = DISABLED
		self.btnStart['state'] = ACTIVE
		self.EntryIP['state'] = NORMAL
		self.EntryPort['state'] = NORMAL

	def do(self):
		isStop = True
		while isStop:
			# send
			sendData(self.dst_ip, self.dst_port)

			#更新界面
			print "send 1"

			time.sleep(1)
			
			#获取进程运行标志
			self.lockSend.acquire()
			isStop = self.bSend
			self.lockSend.release()

		print "Threading is Stop!"


	def myExit(self):
		#修改进程运行标志
		self.lockSend.acquire()
		self.bSend = False
		self.lockSend.release()

		print "Wait for Send threading..."

		self.master.destroy()

if __name__ == '__main__':
	app = Application()
	# 设置窗口标题:
	app.master.title('Tkinter')
	# 自定义结束
	app.master.protocol("WM_DELETE_WINDOW", app.myExit)
	# 主消息循环:
	app.mainloop()