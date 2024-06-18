#define PY_SSIZE_T_CLEAN
#include <Python.h>

#define FTD2XX_EXPORTS
#include <string>
#include <cstdio>
#include <vector>

#include <map>
#include <thread>
#include <chrono>
#include "ftd2xx.h"

#define MUT_BAUDRATE 15625
#define MUT_TIMEOUT 1000
#define OPEN_RETRY_COUNT 10
#define SLEEP_MS(t) (std::this_thread::sleep_for(std::chrono::milliseconds(t)))

#define LOG_VERBOSE 0
#define LOG_INFO 1
#define LOG_WARN 2
#define LOG_ERROR 3

template <typename ... Args>
std::string format(const std::string& fmt, Args ... args ) {
    size_t len = std::snprintf( nullptr, 0, fmt.c_str(), args ... );
    std::vector<char> buf(len + 1);
    std::snprintf(&buf[0], len + 1, fmt.c_str(), args ... );
    return std::string(&buf[0], &buf[0] + len);
}

const std::map<FT_STATUS, std::string> STATUS_STR_TABLE = {
    {FT_OK, "OK"},
    {FT_INVALID_HANDLE, "INVALID_HANDLE"},
    {FT_DEVICE_NOT_FOUND, "DEVICE_NOT_FOUND"},
    {FT_DEVICE_NOT_OPENED, "DEVICE_NOT_OPENED"},
    {FT_IO_ERROR, "IO_ERROR"},
    {FT_INSUFFICIENT_RESOURCES, "INSUFFICIENT_RESOURCES"},
    {FT_INVALID_PARAMETER, "INVALID_PARAMETER"},
    {FT_INVALID_BAUD_RATE, "INVALID_BAUD_RATE"},
    {FT_DEVICE_NOT_OPENED_FOR_ERASE, "DEVICE_NOT_OPENED_FOR_ERASE"},
    {FT_DEVICE_NOT_OPENED_FOR_WRITE, "DEVICE_NOT_OPENED_FOR_WRITE"},
    {FT_FAILED_TO_WRITE_DEVICE, "FAILED_TO_WRITE_DEVICE"},
    {FT_EEPROM_READ_FAILED, "EEPROM_READ_FAILED"},
    {FT_EEPROM_WRITE_FAILED, "EEPROM_WRITE_FAILED"},
    {FT_EEPROM_ERASE_FAILED, "EEPROM_ERASE_FAILED"},
    {FT_EEPROM_NOT_PRESENT, "EEPROM_NOT_PRESENT"},
    {FT_EEPROM_NOT_PROGRAMMED, "EEPROM_NOT_PROGRAMMED"},
    {FT_INVALID_ARGS, "INVALID_ARGS"},
    {FT_NOT_SUPPORTED, "NOT_SUPPORTED"},
    {FT_OTHER_ERROR, "OTHER_ERROR"},
    {FT_DEVICE_LIST_NOT_READY, "DEVICE_LIST_NOT_READY"},
};

/*****************************************************************************
 * Mut Class Definition for Native
 *****************************************************************************/

typedef struct {
    PyObject_HEAD
    FT_HANDLE ftHandle;
    PyObject *logFunctionRef;
} Mut;

// ----------------------------------------------------------------------------
// Output log
// ----------------------------------------------------------------------------
template <typename ... Args>
static void log(Mut *self, int level, const std::string& fmt, Args ... args ) {
    if(self == NULL || self->logFunctionRef == NULL) {
        return;
    }
    
    PyObject *arglist = Py_BuildValue("is", level, format(fmt, args ...).c_str());
    PyObject_CallObject(self->logFunctionRef, arglist);
    Py_XDECREF(arglist);
}

// ----------------------------------------------------------------------------
// build result
// ----------------------------------------------------------------------------
static PyObject* buildResult(FT_STATUS status) {
    return Py_BuildValue("{ss}", "status", STATUS_STR_TABLE.at(status).c_str());
}

// ----------------------------------------------------------------------------
// get device count
// ----------------------------------------------------------------------------
static PyObject* deviceCount(Mut *self) {
    DWORD numDevs = 0;
    FT_STATUS status = FT_ListDevices(&numDevs,NULL,FT_LIST_NUMBER_ONLY);
    return Py_BuildValue("{sssi}", "status", STATUS_STR_TABLE.at(status).c_str(), "value", numDevs);
}

// ----------------------------------------------------------------------------
// Close
// ----------------------------------------------------------------------------
static PyObject* deviceClose(Mut *self) {
    log(self, LOG_VERBOSE, "Mut close...");
    if(self->ftHandle == NULL) {
        return buildResult(FT_DEVICE_NOT_OPENED);
    }
    FT_STATUS status = FT_Close(self->ftHandle);
    self->ftHandle = NULL;
    return buildResult(status);
}

// ----------------------------------------------------------------------------
// Open
// ----------------------------------------------------------------------------
static PyObject* deviceOpen(Mut *self, PyObject *args, PyObject *kwds) {
    log(self, LOG_VERBOSE, "Mut open...");
    if(self->ftHandle != NULL) {
        // ignore error
        deviceClose(self);
    }
    static const char* kwlist[] = {"device_index", NULL};
    int deviceIndex;
    if(!PyArg_ParseTupleAndKeywords(args, kwds, "i", const_cast<char **>(kwlist), &deviceIndex)){
        PyErr_SetString(PyExc_TypeError, "device_index must be integer");
        return Py_BuildValue("");
    }

    FT_STATUS status = FT_Open(deviceIndex, &(self->ftHandle));
    if(!FT_SUCCESS(status)) {
        return buildResult(status);
    }

    status = FT_Purge(self->ftHandle, FT_PURGE_RX | FT_PURGE_TX);
    if(!FT_SUCCESS(status)) {
        return buildResult(status);
    }

    status = FT_SetBaudRate(self->ftHandle, MUT_BAUDRATE);
    if(!FT_SUCCESS(status)) {
        return buildResult(status);
    }

    status = FT_SetDataCharacteristics(self->ftHandle, FT_BITS_8, FT_STOP_BITS_1, FT_PARITY_NONE);
    if(!FT_SUCCESS(status)) {
        return buildResult(status);
    }

    status = FT_SetFlowControl(self->ftHandle, FT_FLOW_NONE, 0, 0);
    if(!FT_SUCCESS(status)) {
        return buildResult(status);
    }

    status = FT_SetTimeouts(self->ftHandle, MUT_TIMEOUT, MUT_TIMEOUT);
    if(!FT_SUCCESS(status)) {
        return buildResult(status);
    }

    UCHAR latencyTimer = 0;
    status = FT_GetLatencyTimer(self->ftHandle, &latencyTimer);
    if(!FT_SUCCESS(status)) {
        return buildResult(status);
    }
    log(self, LOG_VERBOSE, "latencyTimer: %d", latencyTimer);

    status = FT_SetLatencyTimer(self->ftHandle, 1);
    if(!FT_SUCCESS(status)) {
        return buildResult(status);
    }

    status = FT_SetDtr(self->ftHandle);
    if(!FT_SUCCESS(status)) {
        return buildResult(status);
    }
    SLEEP_MS(500);

    status = FT_ClrDtr(self->ftHandle);
    if(!FT_SUCCESS(status)) {
        return buildResult(status);
    }
    SLEEP_MS(740);

    status = FT_SetDtr(self->ftHandle);
    if(!FT_SUCCESS(status)) {
        return buildResult(status);
    }
    SLEEP_MS(600);

    log(self, LOG_VERBOSE, "Mut setup done");

    char req[1] = {0x17};
    DWORD writtenLength = 0;
    char openCheckBuff[2];
    char readBuff[4];
    DWORD returnedLength = 0;

    for(int i = 0; i < OPEN_RETRY_COUNT; i++) {
        memset(openCheckBuff, 0, sizeof(openCheckBuff));
        memset(readBuff, 0, sizeof(readBuff));
        status = FT_Write(self->ftHandle, req, sizeof(req), &writtenLength);
        if(!FT_SUCCESS(status)) {
            return buildResult(status);
        }

        status = FT_Read(self->ftHandle, openCheckBuff, sizeof(openCheckBuff), &returnedLength);
        if(!FT_SUCCESS(status)) {
            return buildResult(status);
        }

        if(openCheckBuff[1] != 0) {  // already open
            log(self, LOG_VERBOSE, "Mut open done");
            return buildResult(status);
        }

        status = FT_SetBreakOn(self->ftHandle);
        if(!FT_SUCCESS(status)) {
            return buildResult(status);
        }
        SLEEP_MS(1800);

        status = FT_SetBreakOff(self->ftHandle);
        if(!FT_SUCCESS(status)) {
            return buildResult(status);
        }

        status = FT_Read(self->ftHandle, readBuff, sizeof(readBuff), &returnedLength);
        if(!FT_SUCCESS(status)) {
            return buildResult(status);
        }
        

        if(readBuff[0] != readBuff[1] && readBuff[2] != readBuff[3]) {
            log(self, LOG_VERBOSE, "Mut open done");
            return buildResult(status);
        } else {
            log(self, LOG_VERBOSE, "MUT open check... %02x,%02x,%02x,%02x", req[0], readBuff[0], readBuff[1], readBuff[2], readBuff[3]);
        }
        log(self, LOG_VERBOSE, "MUT open retry: %d", i);
        SLEEP_MS(10);
    }
    log(self, LOG_VERBOSE, "Mut open failed");
    return buildResult(FT_OTHER_ERROR);
}

// ----------------------------------------------------------------------------
// Request
// ----------------------------------------------------------------------------
static PyObject* requestMut(Mut *self, PyObject *args, PyObject *kwds) {

    log(self, LOG_VERBOSE, "Mut request...");
    if(self->ftHandle == NULL) {
        return buildResult(FT_DEVICE_NOT_OPENED);
    }
    static const char* kwlist[] = {"request_id", NULL};
    UCHAR requestId;
    if(!PyArg_ParseTupleAndKeywords(args, kwds, "b", const_cast<char **>(kwlist), &requestId)){
        PyErr_SetString(PyExc_TypeError, "request_id must be integer");
        return Py_BuildValue("");
    }

    DWORD length = 0;
    FT_STATUS status = FT_Write(self->ftHandle, &requestId, sizeof(UCHAR), &length);
    if(!FT_SUCCESS(status)) {
        return Py_BuildValue("{sssi}", "status", STATUS_STR_TABLE.at(status).c_str(), "value", 0);
    }
    SLEEP_MS(2);

    UCHAR readBuff[2] = {0, 0};
    status = FT_Read(self->ftHandle, readBuff, sizeof(readBuff), &length);
    if(!FT_SUCCESS(status)) {
        return Py_BuildValue("{sssi}", "status", STATUS_STR_TABLE.at(status).c_str(), "value", 0);
    }
    log(self, LOG_VERBOSE, "MUT tx: %02x / rx: %02x,%02x", requestId, readBuff[0], readBuff[1]);
    return Py_BuildValue("{sssi}", "status", STATUS_STR_TABLE.at(status).c_str(), "value", readBuff[1]);
}


/*****************************************************************************
 * Mut Class Definition for Python
 *****************************************************************************/
static void Mut_dealloc(Mut *self) {
    Py_XDECREF(self->logFunctionRef);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject* Mut_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    Mut *self;
    self = (Mut *)type->tp_alloc(type, 0);
    if(self == NULL) {
        return NULL;
    }
    self->logFunctionRef = NULL;
    return (PyObject *)self;
}

static int Mut_init(Mut *self, PyObject *args, PyObject *kwds) {

    static const char* kwlist[] = {"vendor_id", "product_id", "log_func", NULL};
    PyObject *logFunctionRef;
    DWORD vendorId;
    DWORD productId;
    if(!PyArg_ParseTupleAndKeywords(args, kwds, "iiO", const_cast<char **>(kwlist), &vendorId, &productId, &logFunctionRef)){
        return -1;
    }

    if(!PyCallable_Check(logFunctionRef)){
        PyErr_SetString(PyExc_TypeError, "log_func must be callable");
        return -1;
    }
    Py_XSETREF(self->logFunctionRef, Py_NewRef(logFunctionRef));

    log(self, LOG_VERBOSE, "Mut Options VID: %04lx, PID: %04lx", vendorId, productId);
#ifndef WIN32
    FT_SetVIDPID(vendorId, productId);
#endif
    self->ftHandle = NULL;
    return 0;
}

static PyMemberDef Mut_members[] = {
    {NULL}
};

static PyMethodDef Mut_methods[] = {
    {"device_count", (PyCFunction)deviceCount, METH_NOARGS, "Get device count"},
    {"open", (PyCFunction)deviceOpen, METH_VARARGS | METH_KEYWORDS, "open device"},
    {"close", (PyCFunction)deviceClose, METH_NOARGS, "close device"},
    {"request", (PyCFunction)requestMut, METH_VARARGS | METH_KEYWORDS, "request mut"},
    {NULL}
};

static PyTypeObject MutType = {
    .ob_base = PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "mut.Mut",
    .tp_basicsize = sizeof(Mut),
    .tp_itemsize = 0,
    .tp_dealloc = (destructor) Mut_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = PyDoc_STR("MUT class"),
    .tp_methods = Mut_methods,
    .tp_members = Mut_members,
    .tp_init = (initproc) Mut_init,
    .tp_new = Mut_new,
};

static PyModuleDef mut_module = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "mut",
    .m_doc = "MUT module",
    .m_size = -1
};

/*****************************************************************************
 * Module Init
 * do not change the function name.
 *****************************************************************************/
PyMODINIT_FUNC PyInit_mut() {
    PyObject *m;
    if(PyType_Ready(&MutType) < 0) {
        return NULL;
    }
    m = PyModule_Create(&mut_module);
    if(m == NULL) {
        return NULL;
    }

    if (PyModule_AddObject(m, "Mut", (PyObject *)&MutType) < 0) {
        Py_DECREF(m);
        return NULL;
    }
    return m;
}
