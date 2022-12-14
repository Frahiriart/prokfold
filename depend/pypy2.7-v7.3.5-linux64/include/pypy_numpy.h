#include "cpyext_object.h"

#ifdef _WIN64
#define Signed   Py_ssize_t          /* xxx temporary fix */
#define Unsigned unsigned long long  /* xxx temporary fix */
#else
#define Signed   Py_ssize_t     /* xxx temporary fix */
#define Unsigned unsigned long  /* xxx temporary fix */
#endif
        
#define PyArray_CopyInto PyPyArray_CopyInto
PyAPI_FUNC(int) PyArray_CopyInto(struct _object *arg0, struct _object *arg1);
#define PyArray_DescrFromType PyPyArray_DescrFromType
PyAPI_FUNC(struct _object *) PyArray_DescrFromType(Signed arg0);
#define PyUFunc_FromFuncAndData PyPyUFunc_FromFuncAndData
PyAPI_FUNC(struct _object *) PyUFunc_FromFuncAndData(void (**arg0)(char **, Py_ssize_t *, Py_ssize_t *, void *), void *arg1, char *arg2, Signed arg3, Signed arg4, Signed arg5, Signed arg6, char *arg7, char *arg8, Signed arg9);
#define PyUFunc_FromFuncAndDataAndSignature PyPyUFunc_FromFuncAndDataAndSignature
PyAPI_FUNC(struct _object *) PyUFunc_FromFuncAndDataAndSignature(void (**arg0)(char **, Py_ssize_t *, Py_ssize_t *, void *), void *arg1, char *arg2, Signed arg3, Signed arg4, Signed arg5, Signed arg6, char *arg7, char *arg8, Signed arg9, char *arg10);
#define _PyArray_Check _PyPyArray_Check
PyAPI_FUNC(int) _PyArray_Check(struct _object *arg0);
#define _PyArray_CheckExact _PyPyArray_CheckExact
PyAPI_FUNC(int) _PyArray_CheckExact(struct _object *arg0);
#define _PyArray_DATA _PyPyArray_DATA
PyAPI_FUNC(void *) _PyArray_DATA(struct _object *arg0);
#define _PyArray_DIM _PyPyArray_DIM
PyAPI_FUNC(Signed) _PyArray_DIM(struct _object *arg0, Signed arg1);
#define _PyArray_FLAGS _PyPyArray_FLAGS
PyAPI_FUNC(int) _PyArray_FLAGS(struct _object *arg0);
#define _PyArray_FromAny _PyPyArray_FromAny
PyAPI_FUNC(struct _object *) _PyArray_FromAny(struct _object *arg0, struct _object *arg1, Signed arg2, Signed arg3, Signed arg4, void *arg5);
#define _PyArray_FromObject _PyPyArray_FromObject
PyAPI_FUNC(struct _object *) _PyArray_FromObject(struct _object *arg0, Signed arg1, Signed arg2, Signed arg3);
#define _PyArray_ITEMSIZE _PyPyArray_ITEMSIZE
PyAPI_FUNC(int) _PyArray_ITEMSIZE(struct _object *arg0);
#define _PyArray_NBYTES _PyPyArray_NBYTES
PyAPI_FUNC(Signed) _PyArray_NBYTES(struct _object *arg0);
#define _PyArray_NDIM _PyPyArray_NDIM
PyAPI_FUNC(int) _PyArray_NDIM(struct _object *arg0);
#define _PyArray_New _PyPyArray_New
PyAPI_FUNC(struct _object *) _PyArray_New(void *arg0, Signed arg1, Signed *arg2, Signed arg3, Signed *arg4, void *arg5, Signed arg6, Signed arg7, struct _object *arg8);
#define _PyArray_SIZE _PyPyArray_SIZE
PyAPI_FUNC(Signed) _PyArray_SIZE(struct _object *arg0);
#define _PyArray_STRIDE _PyPyArray_STRIDE
PyAPI_FUNC(Signed) _PyArray_STRIDE(struct _object *arg0, Signed arg1);
#define _PyArray_SimpleNew _PyPyArray_SimpleNew
PyAPI_FUNC(struct _object *) _PyArray_SimpleNew(Signed arg0, Signed *arg1, Signed arg2);
#define _PyArray_SimpleNewFromData _PyPyArray_SimpleNewFromData
PyAPI_FUNC(struct _object *) _PyArray_SimpleNewFromData(Signed arg0, Signed *arg1, Signed arg2, void *arg3);
#define _PyArray_SimpleNewFromDataOwning _PyPyArray_SimpleNewFromDataOwning
PyAPI_FUNC(struct _object *) _PyArray_SimpleNewFromDataOwning(Signed arg0, Signed *arg1, Signed arg2, void *arg3);
#define _PyArray_TYPE _PyPyArray_TYPE
PyAPI_FUNC(int) _PyArray_TYPE(struct _object *arg0);
#define PyArray_Type PyPyArray_Type
PyAPI_DATA(PyTypeObject) PyArray_Type;

#undef Signed    /* xxx temporary fix */
#undef Unsigned  /* xxx temporary fix */
