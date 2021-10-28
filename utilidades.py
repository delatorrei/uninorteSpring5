def check_password(Passw):
  vec_passw = ["len(Passw)<8", "len(Passw)>25" , "Passw.isupper()", "Passw.islower()", "Passw.isalpha()",
  "Passw.isdigit()","Passw.isalnum()"]
  for eachValidator in vec_passw:
    if eval(eachValidator):
      print(eachValidator)
      return False
  return True

  