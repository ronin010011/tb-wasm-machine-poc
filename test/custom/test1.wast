(module
 (table 0 anyfunc)
 (memory $0 1)
 (export "memory" (memory $0))
 (export "sum" (func $sum))
 (export "ret10" (func $ret10))
 (export "main" (func $main))
 (func $sum (param $0 i32) (param $1 i32) (result i32)
  (i32.add
   (get_local $1)
   (get_local $0)
  )
 )
 (func $ret10 (result i32)
  (i32.const 10)
 )
 (func $main (result i32)
  (i32.const 20)
 )
)