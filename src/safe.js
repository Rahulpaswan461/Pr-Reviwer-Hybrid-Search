const returnMultipleTwo = ()=>{
    return "2,4"
}

export function calculateSum(){
   const arr = returnMultipleTwo()
   const [a,b] = arr
   return a + b;
}



