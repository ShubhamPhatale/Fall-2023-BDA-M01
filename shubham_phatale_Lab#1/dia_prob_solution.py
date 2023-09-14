inputMessage = input("Enter Input Message:")
def encoder(inputMessage):
    
  currentLetter = ""
  count = 1
  for x in range(1, len(inputMessage)):
    if inputMessage[x] == inputMessage[x - 1]:
      count += 1
    else:
      if count > 1:
        currentLetter += f"{inputMessage[x - 1]}{count}"
      else:
        currentLetter += inputMessage[x - 1]
      count = 1

  if count > 1:
    currentLetter += f"{inputMessage[-1]}{count}"
  else:
    currentLetter += inputMessage[-1]

  return currentLetter

outputMessage = encoder(inputMessage)
print(f"Compressed Message is: {outputMessage}")
