#pragma once

#include "Exception.h"
#include "Isolate.h"
#include "Utils.h"

class CLocker
{
  static bool s_preemption;

  std::auto_ptr<v8::Locker> m_locker;
  CIsolateWrapperPtr m_isolate;

public:
  CLocker() : m_isolate(new CIsolate( util_get_isolate() )) {}
  CLocker(CIsolateWrapperPtr isolate) : m_isolate(isolate)
  {
  }
  bool entered(void) { return NULL != m_locker.get(); }

  void enter(void);
  void leave(void);

  static bool IsLocked();

  static void Expose(void);
};

class CUnlocker
{
  std::auto_ptr<v8::Unlocker> m_unlocker;

public:
  bool entered(void) { return NULL != m_unlocker.get(); }

  void enter(void)
  {
    Py_BEGIN_ALLOW_THREADS

        m_unlocker.reset(new v8::Unlocker( util_get_isolate()));

    Py_END_ALLOW_THREADS
  }
  void leave(void)
  {
    Py_BEGIN_ALLOW_THREADS

        m_unlocker.reset();

    Py_END_ALLOW_THREADS
  }
};
