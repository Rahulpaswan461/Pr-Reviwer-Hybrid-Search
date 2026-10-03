function returnMultipleTwo(){
    return "1,2,3,4"
}

export function calculateSum(){
   const arr = returnMultipleTwo()
   return arr[0] + arr[1]
}

