// libNIDaq.cpp : 定义 DLL 应用程序的导出函数。
//

#include "stdafx.h"
#include<iostream>
#include <stdio.h>
#include <stdlib.h>
#include <NIDAQmx.h>
using namespace std;

extern "C"  __declspec(dllexport) bool init(char * name,int sample,float64 sampleRate,int num);
extern "C"  __declspec(dllexport) bool start();
extern "C"  __declspec(dllexport) bool stop();
extern "C"  __declspec(dllexport) float64 getData(int i);
extern "C"  __declspec(dllexport) int acquireData();
extern "C"  __declspec(dllexport) void finish();
extern "C"  __declspec(dllexport) float64 * getpData();
extern "C"  __declspec(dllexport) float64 getNext();

#define DAQmxErrChk(functionCall) if( DAQmxFailed(error=(functionCall)) ) ; else

int32 num;
int32 sampleNum;
int32 error = 0;
TaskHandle taskHandle = 0;
float64 * data;
int32 read;
char errBuffer[2048];
int numPerChannel;

bool init(char * name,int sample = 1000,float64 sampleRate = 1000.0,int num = 1)
{   
	//char name[20];
	//sprintf(name,"Dev1/ai%i",i);
	cout<<"Name:"<<name<<"haha"<<endl;
	cout<<"sample Rate:"<<sampleRate<<endl;
	numPerChannel = sample/num;
	cout<<"NumPerChannel:"<<numPerChannel<<endl;
	sampleNum = sample;
	cout<<"sample Num:"<<sampleNum<<endl;
	data = new float64[sampleNum];
	DAQmxErrChk (DAQmxCreateTask("",&taskHandle));
	DAQmxErrChk (DAQmxCreateAIVoltageChan(taskHandle,name,"",DAQmx_Val_RSE ,-5,5,DAQmx_Val_Volts,NULL));
	DAQmxErrChk (DAQmxCfgSampClkTiming(taskHandle,"",sampleRate,DAQmx_Val_Rising,DAQmx_Val_ContSamps ,numPerChannel));
	return true;
}

bool start()
{
    DAQmxErrChk (DAQmxStartTask(taskHandle));
	return true;
}

float64 getData(int i)
{
	return data[i];
}

float64 getNext()
{
	if(num < sampleNum)
	{
		return getData(num++);
	}
}

int acquireData()
{
    DAQmxErrChk (DAQmxReadAnalogF64(taskHandle,numPerChannel,3.0,DAQmx_Val_GroupByChannel,data,sampleNum,&read,NULL));
	return read;
}

void getErrInf(char * err = 0)
{
	if( DAQmxFailed(error) )
	{
		DAQmxGetExtendedErrorInfo(errBuffer,2048);
	}
	if(err)
	{
		*err = *errBuffer;
	}
}

float64 * getpData()
{
	return data;
}

bool stop()
{
	if(taskHandle != 0)
	{
		DAQmxErrChk(DAQmxStopTask(taskHandle));
	}
	return 1;
}

void finish()
{
	if( taskHandle!=0 )  
	{
		DAQmxStopTask(taskHandle);
		DAQmxClearTask(taskHandle);
	}
	delete data;
}



class Daq
{
public:
	Daq();
	~Daq();
	bool start();
	bool stop();
	bool initDev();
	int acquireData(int flag);
	void setSampleNum(int num){sampleNum = num;}
	void setDevName(string name){devName = name;}
	void setRate(float64 rate){sampleRate = rate;}
	float64 * getData(){return data;}
private:
	int32 sampleNum;
	int32 error;
	TaskHandle taskHandle;
	float64 sampleRate;
	int32 read;
	string devName;
	float64 * data;
	char *errBuffer;
};

bool Daq::initDev()
{
	DAQmxErrChk (DAQmxCreateTask("",&taskHandle));
	DAQmxErrChk (DAQmxCreateAIVoltageChan(taskHandle,devName.data(),"",DAQmx_Val_RSE ,-5,5,DAQmx_Val_Volts,NULL));
	DAQmxErrChk (DAQmxCfgSampClkTiming(taskHandle,"",sampleRate,DAQmx_Val_Rising,DAQmx_Val_ContSamps ,sampleNum));
	return true;
}

Daq::Daq()
{
	sampleNum = 1000;
	error = 0;
	taskHandle = 0;
	sampleRate = 1000.0;
	read = 0;
	devName = "Dev1/ai0";
}

Daq::~Daq()
{
	if( taskHandle!=0 )  
	{
		stop();
		DAQmxClearTask(taskHandle);
	}
	delete [] data;
	delete [] errBuffer;
}

bool Daq::start()
{
	DAQmxErrChk (DAQmxStartTask(taskHandle));
	return true;
}

bool Daq::stop()
{
	if(taskHandle != 0)
	{
		DAQmxErrChk (DAQmxStopTask(taskHandle));
	}
	return true;
}

int Daq::acquireData(int flag = 0)
{
	bool32 fillMode;
	if(flag == 0)
	{
		fillMode = DAQmx_Val_GroupByChannel;
	}
	else
	{
		fillMode = DAQmx_Val_GroupByScanNumber ;
	}
    DAQmxErrChk (DAQmxReadAnalogF64(taskHandle,sampleNum,3.0,fillMode,data,sampleNum,&read,NULL));
	return read;
}

