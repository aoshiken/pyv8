#pragma once

#include <functional>

#include <boost/shared_ptr.hpp>

#include "Wrapper.h"
#include "Utils.h"

class CContext final
{
  v8::Persistent<v8::Context> m_context;
  py::object m_global;

private: // Embeded Data
  enum EmbedderDataFields
  {
    DebugIdIndex = v8::Context::kDebugIdIndex,
    LoggerIndex,
    GlobalObjectIndex,
  };

  template <typename T>
  static T *GetEmbedderData(v8::Handle<v8::Context> context, EmbedderDataFields index, std::function<T *()> creator = nullptr)
  {
    assert(!context.IsEmpty());
    assert(index > DebugIdIndex);

    auto value = static_cast<T *>(v8::Handle<v8::External>::Cast(context->GetEmbedderData(index))->Value());

    if (!value && creator)
    {
      value = creator();

      SetEmbedderData(context, index, value);
    }

    return value;
  }

  template <typename T>
  static void SetEmbedderData(v8::Handle<v8::Context> context, EmbedderDataFields index, T *data)
  {
    assert(!context.IsEmpty());
    assert(index > DebugIdIndex);
    assert(data);

    context->SetEmbedderData(index, v8::External::New(context->GetIsolate(), (void *)data));
  }


public:
  CContext(v8::Handle<v8::Context> context, v8::Isolate *isolate = util_get_isolate());
  CContext(const CContext &context, v8::Isolate *isolate = util_get_isolate());
  CContext(py::object global, py::list extensions, v8::Isolate *isolate = util_get_isolate());
  ~CContext() { Dispose(); }

  void Dispose();

  inline v8::Handle<v8::Context> Context(v8::Isolate *isolate = util_get_isolate()) const { return m_context.Get(isolate); }

  py::object GetGlobal(void) const;

  py::str GetSecurityToken(void) const;
  void SetSecurityToken(py::str token);

  bool IsEntered(void) const { return !m_context.IsEmpty(); }

  void Enter(void);
  void Leave(void);

  py::object Evaluate(const std::string &src, const std::string name = std::string(), int line = -1, int col = -1);
  py::object EvaluateW(const std::wstring &src, const std::string name = std::string(), int line = -1, int col = -1);

  static py::object GetEntered( void );
  static py::object GetCurrent(v8::Isolate *isolate = util_get_isolate());
  static py::object GetCalling(v8::Isolate *isolate = util_get_isolate());

  static bool InContext(v8::Isolate *isolate = util_get_isolate()) { return isolate->InContext(); }

  static void Expose(void);
};

typedef boost::shared_ptr<CContext> CContextPtr;
