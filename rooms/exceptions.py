from rest_framework.views import exception_handler

def global_exception_handler(exc, context):
  response = exception_handler(exc, context)

  if response is not None: 
    exception_msg = list(response.data.values())[0][0]
    
    response.data = {
      'status_code': response.status_code,
      'msg': exception_msg,
      'error': True
    }  
    
  return response