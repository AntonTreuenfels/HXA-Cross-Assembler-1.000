

! Test Templates


!! Templates
- <A HREF="..\test\test000.a">..\test\test000.a</A>
- ok: tests should succeed; check response to correct input
- <A HREF="..\test\test000e.a">..\test\test000e.a</A>
- error: tests should fail; check response to incorrect input


! Comments


!! All Forms
- <A HREF="..\test\test001.a">..\test\test001.a</A>
- ok: comments
- <A HREF="..\test\test001e.a">..\test\test001e.a</A>
- error: comments


! Required


!! Set CPU
- <A HREF="..\test\test002.a">..\test\test002.a</A>
- ok: "CPU" psop (16-bit Processor)
- <A HREF="..\test\test002b.a">..\test\test002b.a</A>
- ok: "CPU" psop (24-bit Processor)
- <A HREF="..\test\test002c.a">..\test\test002c.a</A>
- ok: "CPU" psop (32-bit Processor)
- <A HREF="..\test\test002d.a">..\test\test002d.a</A>
- ok: "CPU" psop - undelimited descriptor
- <A HREF="..\test\test002e.a">..\test\test002e.a</A>
- error\fatal: missing "CPU" psop
- <A HREF="..\test\test002f.a">..\test\test002f.a</A>
- warn\error: unknown CPU; unique CPU
- <A HREF="..\test\test002g.a">..\test\test002g.a</A>
- warn/error/fatal: pc width too small
- <A HREF="..\test\test002h.a">..\test\test002h.a</A>
- warn/error/fatal: pc width too large


!! Set Program Counter
- <A HREF="..\test\test003.a">..\test\test003.a</A>
- ok: "ORG" psop
- <A HREF="..\test\test003b.a">..\test\test003b.a</A>
- ok: "ORG" psop (24-bit Processor)
- <A HREF="..\test\test003c.a">..\test\test003c.a</A>
- ok: "ORG" psop (32-bit Processor)
- <A HREF="..\test\test003e.a">..\test\test003e.a</A>
- fatal: missing "ORG"
- <A HREF="..\test\test003f.a">..\test\test003f.a</A>
- fatal: unintialized program counter
- <A HREF="..\test\test003g.a">..\test\test003g.a</A>
- error\fatal: missing expression
- <A HREF="..\test\test003h.a">..\test\test003h.a</A>
- warn\error\fatal: 16-bit PC out of range (negative)
- <A HREF="..\test\test003i.a">..\test\test003i.a</A>
- error\fatal: 16-bit PC out of range (too big; by ORG)
- <A HREF="..\test\test003j.a">..\test\test003j.a</A>
- error\fatal: 16-bit PC out of range (too big; by pc advance)
- <A HREF="..\test\test003k.a">..\test\test003k.a</A>
- warn\error\fatal: 24-bit PC out of range (negative)
- <A HREF="..\test\test003l.a">..\test\test003l.a</A>
- error\fatal: 24-bit PC out of range (too big; by ORG)
- <A HREF="..\test\test003m.a">..\test\test003m.a</A>
- error\fatal: 24-bit PC out of range (too big; by pc advance)
- <A HREF="..\test\test003n.a">..\test\test003n.a</A>
- warn\error\fatal: 32-bit PC out of range (negative)
- <A HREF="..\test\test003o.a">..\test\test003o.a</A>
- error\fatal: 32-bit PC out of range (too big; by ORG)
- <A HREF="..\test\test003p.a">..\test\test003p.a</A>
- error\fatal: 32-bit PC out of range (too big; by pc advance)


! Messages


!! User Messages
- <A HREF="..\test\test005.a">..\test\test005.a</A>
- echo\ok: "ECHO" psop
- <A HREF="..\test\test005e.a">..\test\test005e.a</A>
- warn: "ECHO" psop
- <A HREF="..\test\test005f.a">..\test\test005f.a</A>
- warn: "WARN" psop
- <A HREF="..\test\test005g.a">..\test\test005g.a</A>
- warn\error: "ERROR" psop
- <A HREF="..\test\test005h.a">..\test\test005h.a</A>
- fatal: "FATAL" psop
- <A HREF="..\test\test005i.a">..\test\test005i.a</A>
- fatal: "FATAL" psop
- <A HREF="..\test\test005j.a">..\test\test005j.a</A>
- warn\fatal: "FATAL" psop
- <A HREF="..\test\test005k.a">..\test\test005k.a</A>
- warn: "WARN" psop


!! Warn Count
- <A HREF="..\test\test006e.a">..\test\test006e.a</A>
- warn\fatal: "MAXWARN" psop set to negative value
- <A HREF="..\test\test006f.a">..\test\test006f.a</A>
- warn\fatal: "MAXWARN" psop set to zero
- <A HREF="..\test\test006g.a">..\test\test006g.a</A>
- warn\fatal: "MAXWARN" psop set to one
- <A HREF="..\test\test006h.a">..\test\test006h.a</A>
- warn\fatal: "MAXWARN" psop set to three


!! Error Count
- <A HREF="..\test\test007e.a">..\test\test007e.a</A>
- warn\error\fatal: "MAXERR" psop set to negative value
- <A HREF="..\test\test007f.a">..\test\test007f.a</A>
- error\fatal: "MAXERR" psop set to zero
- <A HREF="..\test\test007g.a">..\test\test007g.a</A>
- error\fatal: "MAXERR" psop set to one
- <A HREF="..\test\test007h.a">..\test\test007h.a</A>
- error\fatal: "MAXERR" psop set to three


!! Assert Messages
- <A HREF="..\test\test008.a">..\test\test008.a</A>
- ok: "ASSERT" psop
- <A HREF="..\test\test008e.a">..\test\test008e.a</A>
- error: failures detected on first pass
- <A HREF="..\test\test008f.a">..\test\test008f.a</A>
- error: failures detected on second pass
- <A HREF="..\test\test008g.a">..\test\test008g.a</A>
- error: failures detected on first pass (BDD1)


! Output Files


!! Same Directory
- <A HREF="..\test\test010.a">..\test\test010.a</A>
- ok: specified names
- <A HREF="..\test\test010b.a">..\test\test010b.a</A>
- ok: default extensions
- <A HREF="..\test\test010c.a">..\test\test010c.a</A>
- ok: default filenames given only directories
- <A HREF="..\test\test010d.a">..\test\test010d.a</A>
- ok: template filename with default extension
- <A HREF="..\test\test010e.a">..\test\test010e.a</A>
- warn\error: malformed name
- <A HREF="..\test\test010f.a">..\test\test010f.a</A>
- warn\error: name changed
- <A HREF="..\test\test010g.a">..\test\test010g.a</A>
- warn: problematic characters in names
- <A HREF="..\test\test010h.a">..\test\test010h.a</A>
- error: output filename same as existing ouput filename
- <A HREF="..\test\test010i.a">..\test\test010i.a</A>
- warn: output filename same as input filename (first pass)


!! Other Directory
- <A HREF="..\test\test011.a">..\test\test011.a</A>
- ok: specified name
- <A HREF="..\test\test011b.a">..\test\test011b.a</A>
- ok: different device
- <A HREF="..\test\test011e.a">..\test\test011e.a</A>
- error: non-existent list/object directories
- <A HREF="..\test\test011f.a">..\test\test011f.a</A>
- error: non-existent error directory


!! No Object Code
- <A HREF="..\test\test014.a">..\test\test014.a</A>
- ok: no object code


!! No List or Error Files
- <A HREF="..\test\test014b.a">..\test\test014b.a</A>
- ok: no output files


!! No Error File
- <A HREF="..\test\test014c.a">..\test\test014c.a</A>
- ok: error found but no error file to write


! Pass Termination


!! Termination
- <A HREF="..\test\test015.a">..\test\test015.a</A>
- ok: "END" psop
- <A HREF="..\test\test015e.a">..\test\test015e.a</A>
- error: "END" w/ un-resolvable start expression
- <A HREF="..\test\test015f.a">..\test\test015f.a</A>
- error: "END" w/ resolvable start expression but no CPU defined
- <A HREF="..\test\test015g.a">..\test\test015g.a</A>
- error: "END" w/ resolvable start expression out of range


! Customization


!! Pseudo Op Names
- <A HREF="..\test\test020.a">..\test\test020.a</A>
- ok: "PSALIAS" pseudo-op
- <A HREF="..\test\test020b.a">..\test\test020b.a</A>
- ok: "PSALIAS" pseudo-op (undelimited arguments)
- <A HREF="..\test\test020e.a">..\test\test020e.a</A>
- error: malformed "PSALIAS" pseudo-op


!! Pseudo Op Nullification
- <A HREF="..\test\test021.a">..\test\test021.a</A>
- ok: "PSNULL" pseudo op
- <A HREF="..\test\test021e.a">..\test\test021e.a</A>
- error: "PSNULL" pseudo op (when not used)


!! Assembler Messages
- <A HREF="..\test\test022.a">..\test\test022.a</A>
- ok: "MESGTEXT" pseudo-op
- <A HREF="..\test\test022e.a">..\test\test022e.a</A>
- warn\error: malformed "MESGTEXT" pseudo-op


!! ASSUME Strings
- <A HREF="..\test\test025.a">..\test\test025.a</A>
- ok: "ASSUME" pseudo-op
- <A HREF="..\test\test025b.a">..\test\test025b.a</A>
- ok: "ASSUME" pseudo-op (Octet Extraction Order)
- <A HREF="..\test\test025e.a">..\test\test025e.a</A>
- error: unrecognized flag and arg value


! Expressions


!! Numeric Literals
- <A HREF="..\test\test035.a">..\test\test035.a</A>
- ok: Motorola, Intel and C formats (LSB Processor)
- <A HREF="..\test\test035b.a">..\test\test035b.a</A>
- ok: Motorola, Intel and C formats (MSB Processor)
- <A HREF="..\test\test035e.a">..\test\test035e.a</A>
- error: malformed numeric literals
- <A HREF="..\test\test035f.a">..\test\test035f.a</A>
- error: malformed Intel numbers (during pass two)
- <A HREF="..\test\test035g.a">..\test\test035g.a</A>
- warn: out of range numbers (signed integers more than 32 bits in size)


!! Numeric Data Definition
- <A HREF="..\test\test036.a">..\test\test036.a</A>
- ok: "BIT--" pseudo ops
- <A HREF="..\test\test036b.a">..\test\test036b.a</A>
- ok: "BIT--" pseudo ops (MSB Processor)
- <A HREF="..\test\test036e.a">..\test\test036e.a</A>
- error: blank expression field(s)


!! Ranged Numeric Data Definition
- <A HREF="..\test\test037.a">..\test\test037.a</A>
- ok: "UBIT--" and "SBIT--" pseudo ops
- <A HREF="..\test\test037b.a">..\test\test037b.a</A>
- ok: "UBIT--" and "SBIT--" pseudo ops (MSB Processor)
- <A HREF="..\test\test037e.a">..\test\test037e.a</A>
- error: values out of range (pass two)
- <A HREF="..\test\test037f.a">..\test\test037f.a</A>
- error: values out of range (pass two)


!! Character Literals
- <A HREF="..\test\test040.a">..\test\test040.a</A>
- ok: character literals
- <A HREF="..\test\test040b.a">..\test\test040b.a</A>
- ok: Unicode character literals
- <A HREF="..\test\test040e.a">..\test\test040e.a</A>
- error: malformed characters


!! String Literals
- <A HREF="..\test\test045.a">..\test\test045.a</A>
- ok: string literals
- <A HREF="..\test\test045b.a">..\test\test045b.a</A>
- ok: object code string storage
- <A HREF="..\test\test045c.a">..\test\test045c.a</A>
- ok: ECHO string literals w/ unprintable chars
- <A HREF="..\test\test045e.a">..\test\test045e.a</A>
- error: malformed strings


!! XLATE() and XLATE
- <A HREF="..\test\test046.a">..\test\test046.a</A>
- ok: character set re-mapping
- <A HREF="..\test\test046b.a">..\test\test046b.a</A>
- ok: character set re-mapping
- <A HREF="..\test\test046e.a">..\test\test046e.a</A>
- warn\error: malformed translation patterns
- <A HREF="..\test\test046f.a">..\test\test046f.a</A>
- error: malformed char translation function
- <A HREF="..\test\test046g.a">..\test\test046g.a</A>
- error: reserved name
- <A HREF="..\test\test046h.a">..\test\test046h.a</A>
- error: reserved name


!! Global Labels
- <A HREF="..\test\test050.a">..\test\test050.a</A>
- ok: global labels
- <A HREF="..\test\test050e.a">..\test\test050e.a</A>
- error: malformed global labels
- <A HREF="..\test\test050f.a">..\test\test050f.a</A>
- error: global labels (non-existent)
- <A HREF="..\test\test050g.a">..\test\test050g.a</A>
- error: global label ok; rest of source line malformed
- <A HREF="..\test\test050h.a">..\test\test050h.a</A>
- error: duplicate labels


!! Local Labels
- <A HREF="..\test\test051.a">..\test\test051.a</A>
- ok: local labels
- <A HREF="..\test\test051b.a">..\test\test051b.a</A>
- ok: local labels
- <A HREF="..\test\test051e.a">..\test\test051e.a</A>
- error: missing local label (backward ref)
- <A HREF="..\test\test051f.a">..\test\test051f.a</A>
- error: missing local label (forward ref)
- <A HREF="..\test\test051g.a">..\test\test051g.a</A>
- error: duplicate labels


!! Variable Labels
- <A HREF="..\test\test052.a">..\test\test052.a</A>
- ok: variable labels
- <A HREF="..\test\test052e.a">..\test\test052e.a</A>
- warn: odd use (forward reference successfully resolved)
- <A HREF="..\test\test052f.a">..\test\test052f.a</A>
- warn\error: odd use (forward reference unsuccessfully resolved)


!! Branch Target Labels
- <A HREF="..\test\test053.a">..\test\test053.a</A>
- ok: branch target labels
- <A HREF="..\test\test053b.a">..\test\test053b.a</A>
- ok: colons as synomyms for "+-" and "-+" labels
- <A HREF="..\test\test053c.a">..\test\test053c.a</A>
- ok: only colons as branch targets
- <A HREF="..\test\test053e.a">..\test\test053e.a</A>
- error: malformed branch target labels
- <A HREF="..\test\test053f.a">..\test\test053f.a</A>
- error: missing labels (forward reference)
- <A HREF="..\test\test053g.a">..\test\test053g.a</A>
- warn: odd use (with various pseudo ops)


!! All Label Forms
- <A HREF="..\test\test054.a">..\test\test054.a</A>
- ok: label recognition; all forms


!! String Labels
- <A HREF="..\test\test055.a">..\test\test055.a</A>
- ok: string and numeric labels (all forms)
- <A HREF="..\test\test055e.a">..\test\test055e.a</A>
- error: string labels


!! Pre-Defined Labels
- <A HREF="..\test\test056.a">..\test\test056.a</A>
- ok: string and numeric labels
- <A HREF="..\test\test056e.a">..\test\test056e.a</A>
- error: string and numeric labels


!! Program Counter Reference
- <A HREF="..\test\test060.a">..\test\test060.a</A>
- ok: program counter (w/aliases)
- <A HREF="..\test\test060e.a">..\test\test060e.a</A>
- error: "*" and "$" aliases not legal in label field


!! Program Counter Relative Numeric Data Definition
- <A HREF="..\test\test067.a">..\test\test067.a</A>
- ok: "RBIT--" pseudo ops
- <A HREF="..\test\test067e.a">..\test\test067e.a</A>
- error: value out of relative range
- <A HREF="..\test\test067f.a">..\test\test067f.a</A>
- error: value out of program counter range


!! Unary Operators
- <A HREF="..\test\test080.a">..\test\test080.a</A>
- ok: arithmetic, bitwise, logical
- <A HREF="..\test\test080b.a">..\test\test080b.a</A>
- ok: arithmetic, bitwise, logical (string operands)
- <A HREF="..\test\test080e.a">..\test\test080e.a</A>
- error: malformed expressions
- <A HREF="..\test\test080f.a">..\test\test080f.a</A>
- error: out-of-range values


!! Numeric Binary Operators
- <A HREF="..\test\test081.a">..\test\test081.a</A>
- ok: arithmetic, bitwise, logical
- <A HREF="..\test\test081e.a">..\test\test081e.a</A>
- error: malformed expressions
- <A HREF="..\test\test081f.a">..\test\test081f.a</A>
- error: out-of-range values
- <A HREF="..\test\test081g.a">..\test\test081g.a</A>
- error: modulus by zero
- <A HREF="..\test\test081h.a">..\test\test081h.a</A>
- error: bad shift values


!! String Binary Operators
- <A HREF="..\test\test082.a">..\test\test082.a</A>
- ok: logical
- <A HREF="..\test\test082b.a">..\test\test082b.a</A>
- ok: concatenation
- <A HREF="..\test\test082c.a">..\test\test082c.a</A>
- ok: mutliplication
- <A HREF="..\test\test082e.a">..\test\test082e.a</A>
- error: malformed expressions
- <A HREF="..\test\test082f.a">..\test\test082f.a</A>
- error: string concatenation
- <A HREF="..\test\test082g.a">..\test\test082g.a</A>
- error: multiplication


!! Regular Expression Operators
- <A HREF="..\test\test083.a">..\test\test083.a</A>
- ok: logical
- <A HREF="..\test\test083b.a">..\test\test083b.a</A>
- ok: EQU psop
- <A HREF="..\test\test083c.a">..\test\test083c.a</A>
- ok: syntax
- <A HREF="..\test\test083e.a">..\test\test083e.a</A>
- error: malformed expressions
- <A HREF="..\test\test083f.a">..\test\test083f.a</A>
- error: EQU psop


!! String Expressions
- <A HREF="..\test\test084.a">..\test\test084.a</A>
- ok: string concatenation
- <A HREF="..\test\test084e.a">..\test\test084e.a</A>
- error: string concatenation


!! Logical Short Circuit
- <A HREF="..\test\test085.a">..\test\test085.a</A>
- ok: "&&" and "||" Operators
- <A HREF="..\test\test085b.a">..\test\test085b.a</A>
- ok: "&&" and "||" Operators (string expressions)
- <A HREF="..\test\test085c.a">..\test\test085c.a</A>
- ok: "&&" and "||" Operators (mixed expressions)
- <A HREF="..\test\test085d.a">..\test\test085d.a</A>
- ok: "&&" and "||" Operators (left side forward-referenced)
- <A HREF="..\test\test085e.a">..\test\test085e.a</A>
- error: unresolvable "&&" and "||" Operators


!! Ternary Conditional
- <A HREF="..\test\test086.a">..\test\test086.a</A>
- ok: "?:" Operator
- <A HREF="..\test\test086b.a">..\test\test086b.a</A>
- ok: "?:" Operator, Forward Reference
- <A HREF="..\test\test086e.a">..\test\test086e.a</A>
- error: parse errors
- <A HREF="..\test\test086f.a">..\test\test086f.a</A>
- error: bad forward reference (pass 2)
- <A HREF="..\test\test086g.a">..\test\test086g.a</A>
- error: bad forward reference (pass 1)


!! Expression Evaluation
- <A HREF="..\test\test090.a">..\test\test090.a</A>
- ok: expression evaluation
- <A HREF="..\test\test090b.a">..\test\test090b.a</A>
- ok: expression evaluation (MSB processor)
- <A HREF="..\test\test090e.a">..\test\test090e.a</A>
- error: malformed expressions
- <A HREF="..\test\test090f.a">..\test\test090f.a</A>
- error: out-of-range values
- <A HREF="..\test\test090g.a">..\test\test090g.a</A>
- error: divide by zero
- <A HREF="..\test\test090h.a">..\test\test090h.a</A>
- warn\error: multiple unresolved forward reference in single expression


!! Assign Label Value
- <A HREF="..\test\test092.a">..\test\test092.a</A>
- ok: "EQU" psop
- <A HREF="..\test\test092b.a">..\test\test092b.a</A>
- ok: "EQU" psop (all label type values shown in object section)
- <A HREF="..\test\test092c.a">..\test\test092c.a</A>
- ok: "PLUSEQU" and "MINUSEQU" psops
- <A HREF="..\test\test092e.a">..\test\test092e.a</A>
- error: bad "EQU" use
- <A HREF="..\test\test092f.a">..\test\test092f.a</A>
- error: "PLUSEQU" and "MINUSEQU" psops


! Macros


!! Macro Definition
- <A HREF="..\test\test100.a">..\test\test100.a</A>
- ok: basic macro definition and expansion
- <A HREF="..\test\test100b.a">..\test\test100b.a</A>
- ok: basic macro definition and expansion (default listing)
- <A HREF="..\test\test100c.a">..\test\test100c.a</A>
- ok: basic macro definition and expansion (string names)
- <A HREF="..\test\test100e.a">..\test\test100e.a</A>
- warn\error: basic macro definition
- <A HREF="..\test\test100f.a">..\test\test100f.a</A>
- warn\error: basic macro expansion
- <A HREF="..\test\test100g.a">..\test\test100g.a</A>
- error: error in body of definition (first pass)
- <A HREF="..\test\test100h.a">..\test\test100h.a</A>
- error: unresolved forward reference within macro (second pass)


!! Nested Macros
- <A HREF="..\test\test101.a">..\test\test101.a</A>
- ok: nested macro definitions
- <A HREF="..\test\test101b.a">..\test\test101b.a</A>
- ok: nested macro definitions (default listing)
- <A HREF="..\test\test101e.a">..\test\test101e.a</A>
- error: nested macro definition
- <A HREF="..\test\test101f.a">..\test\test101f.a</A>
- error: error in body of definition (first pass)
- <A HREF="..\test\test101g.a">..\test\test101g.a</A>
- error: unresolved forward reference within nested macro (first pass)


!! EXIT from Macro
- <A HREF="..\test\test103.a">..\test\test103.a</A>
- ok: unconditional "EXIT" psop within macro
- <A HREF="..\test\test103b.a">..\test\test103b.a</A>
- ok: unconditional "EXIT" psop within macro (labelled endpoint)
- <A HREF="..\test\test103e.a">..\test\test103e.a</A>
- warn\error: unconditional "EXIT" outside of macro


!! EXITIF from Macro
- <A HREF="..\test\test104.a">..\test\test104.a</A>
- ok: conditional exit psop within macro (all TRUE)
- <A HREF="..\test\test104b.a">..\test\test104b.a</A>
- ok: conditional exit psop within macro (all FALSE)
- <A HREF="..\test\test104e.a">..\test\test104e.a</A>
- warn\error: unconditional "EXIT" outside of macro


!! DEFINED() and UNDEF
- <A HREF="..\test\test105.a">..\test\test105.a</A>
- ok: macro definition existence testing and deletion
- <A HREF="..\test\test105e.a">..\test\test105e.a</A>
- error: malformed "defined()" function and "undef" psop
- <A HREF="..\test\test105f.a">..\test\test105f.a</A>
- error: illegal DEFINED() argument value
- <A HREF="..\test\test105g.a">..\test\test105g.a</A>
- error: illegal UNDEF variable name


!! Macros and Labels
- <A HREF="..\test\test106.a">..\test\test106.a</A>
- ok: macros with the same names as labels
- <A HREF="..\test\test106e.a">..\test\test106e.a</A>
- error: macros with the same names as labels


!! Odd Macro Arguments
- <A HREF="..\test\test107.a">..\test\test107.a</A>
- ok: actual arguments which match formal argument names


!! Default Macro Arguments
- <A HREF="..\test\test110.a">..\test\test110.a</A>
- ok: macros with default argument values
- <A HREF="..\test\test110e.a">..\test\test110e.a</A>
- error: malformed macro defaults


!! PUTBACK pseudo op
- <A HREF="..\test\test112.a">..\test\test112.a</A>
- ok: "PUTBACK" psop
- <A HREF="..\test\test112e.a">..\test\test112e.a</A>
- warn\error: "PUTBACK" psop


!! PUTBACKS pseudo op
- <A HREF="..\test\test113.a">..\test\test113.a</A>
- ok: "PUTBACKS" psop
- <A HREF="..\test\test113e.a">..\test\test113e.a</A>
- warn\error: "PUTBACKS" psop
- <A HREF="..\test\test113f.a">..\test\test113f.a</A>
- fatal: maximum putback count exceeded


!! Assignable Formal Arguments
- <A HREF="..\test\test115.a">..\test\test115.a</A>
- ok: local and variable label names used as formal macro arguments
- <A HREF="..\test\test115b.a">..\test\test115b.a</A>
- ok: object listing shows full macro expansion and all equate values
- <A HREF="..\test\test115e.a">..\test\test115e.a</A>
- error: definition errors
- <A HREF="..\test\test115f.a">..\test\test115f.a</A>
- error: forward reference (fail) and backward reference (ok)


! Local Scope


!! Nesting Depth
- <A HREF="..\test\test125e.a">..\test\test125e.a</A>
- warn\fatal: "MAXDEPTH" psop set to negative value
- <A HREF="..\test\test125f.a">..\test\test125f.a</A>
- warn\fatal: "MAXDEPTH" psop set to zero
- <A HREF="..\test\test125g.a">..\test\test125g.a</A>
- warn\fatal: "MAXDEPTH" psop set to one
- <A HREF="..\test\test125h.a">..\test\test125h.a</A>
- warn\fatal: "MAXDEPTH" psop set to three


! Repeats


!! Repeat Definition
- <A HREF="..\test\test150.a">..\test\test150.a</A>
- ok: basic repeat block definition and expansion
- <A HREF="..\test\test150b.a">..\test\test150b.a</A>
- ok: no expansion if less than one
- <A HREF="..\test\test150e.a">..\test\test150e.a</A>
- warn\error: repeat block definition errors
- <A HREF="..\test\test150f.a">..\test\test150f.a</A>
- warn\error: repeat block expansion errors
- <A HREF="..\test\test150g.a">..\test\test150g.a</A>
- error: unresolved forward reference within repeat


!! Macros and Repeats
- <A HREF="..\test\test151.a">..\test\test151.a</A>
- ok: repeats within macros
- <A HREF="..\test\test151e.a">..\test\test151e.a</A>
- error: macro definitions within repeat blocks
- <A HREF="..\test\test151f.a">..\test\test151f.a</A>
- error: crossed macro/repeat blocks (variation 1)
- <A HREF="..\test\test151g.a">..\test\test151g.a</A>
- error: crossed macro/repeat blocks (variation 2)
- <A HREF="..\test\test151h.a">..\test\test151h.a</A>
- error: non-constant repeat control expression within macro expansion


!! EXIT from Repeat
- <A HREF="..\test\test153.a">..\test\test153.a</A>
- ok: unconditional "EXIT" psop within repeat block


!! EXIT from Nested Macro/Repeats
- <A HREF="..\test\test155.a">..\test\test155.a</A>
- ok: unconditional "EXIT" from nested macro/repeat blocks


!! Repeat Count
- <A HREF="..\test\test157e.a">..\test\test157e.a</A>
- fatal: too many repeats


! Whiles


!! While Definition
- <A HREF="..\test\test160.a">..\test\test160.a</A>
- ok: basic while block definition and expansion (numeric control expressions)
- <A HREF="..\test\test160b.a">..\test\test160b.a</A>
- ok: basic while block definition and expansion (string control expressions)
- <A HREF="..\test\test160e.a">..\test\test160e.a</A>
- warn\error: while block definition errors
- <A HREF="..\test\test160f.a">..\test\test160f.a</A>
- warn\error: while block expansion errors
- <A HREF="..\test\test160g.a">..\test\test160g.a</A>
- error: unresolved forward reference within while
- <A HREF="..\test\test160h.a">..\test\test160h.a</A>
- error: crossed WHILE and REPEAT blocks
- <A HREF="..\test\test160i.a">..\test\test160i.a</A>
- error: storage expression goes out of range


!! Macros and Whiles
- <A HREF="..\test\test161.a">..\test\test161.a</A>
- ok: whiles within macros
- <A HREF="..\test\test161e.a">..\test\test161e.a</A>
- error: macro definitions within while blocks
- <A HREF="..\test\test161f.a">..\test\test161f.a</A>
- error: crossed macro/while blocks (variation 1)
- <A HREF="..\test\test161g.a">..\test\test161g.a</A>
- error: crossed macro/while blocks (variation 2)
- <A HREF="..\test\test161h.a">..\test\test161h.a</A>
- error: non-constant while control expression within macro expansion


!! EXIT from While
- <A HREF="..\test\test163.a">..\test\test163.a</A>
- ok: unconditional "EXIT" psop within while block


!! EXIT from Nested Macro/Whiles
- <A HREF="..\test\test165.a">..\test\test165.a</A>
- ok: unconditional "EXIT" from nested macro/while blocks


!! While Count
- <A HREF="..\test\test167e.a">..\test\test167e.a</A>
- fatal: too many whiles


! Conditional Assembly


!! IF..ELSEIF..ELSE..ENDIF Blocks
- <A HREF="..\test\test200.a">..\test\test200.a</A>
- ok: IF..ELSEIF..ELSE..ENDIF conditionals
- <A HREF="..\test\test200b.a">..\test\test200b.a</A>
- ok: IF..ELSEIF..ELSE..ENDIF conditionals (string expressions)
- <A HREF="..\test\test200c.a">..\test\test200c.a</A>
- ok: IF..ELSEIF..ELSE..ENDIF conditionals / list false branches
- <A HREF="..\test\test200e.a">..\test\test200e.a</A>
- warning\error: malformed conditionals
- <A HREF="..\test\test200f.a">..\test\test200f.a</A>
- error: unclosed conditional blocks within macros
- <A HREF="..\test\test200g.a">..\test\test200g.a</A>
- error: no forward reference in conditional
- <A HREF="..\test\test200h.a">..\test\test200h.a</A>
- error: crossed macro/if blocks


!! Odd Conditional Blocks
- <A HREF="..\test\test201.a">..\test\test201.a</A>
- ok: odd but legal uses of conditional assembly blocks


!! EXIT Inside Conditional
- <A HREF="..\test\test203.a">..\test\test203.a</A>
- ok: "EXIT" from macros inside nested conditionals


!! Deep Nesting
- <A HREF="..\test\test205.a">..\test\test205.a</A>
- ok: recursive macros; depth = 128


!! IFDEF and IFNDEF Blocks
- <A HREF="..\test\test210.a">..\test\test210.a</A>
- ok: IFDEF and INDEF conditionals (for symbols)
- <A HREF="..\test\test210e.a">..\test\test210e.a</A>
- warning\error: malformed conditionals
- <A HREF="..\test\test210f.a">..\test\test210f.a</A>
- error: undetected errors


! File Inclusion


!! Inclusion
- <A HREF="..\test\test250.a">..\test\test250.a</A>
- ok: file inclusion; depth = 128
- <A HREF="..\test\test250e.a">..\test\test250e.a</A>
- warn\error: malformed "INCLUDE"
- <A HREF="..\test\test250f.a">..\test\test250f.a</A>
- error: unclosed IF conditional in include file
- <A HREF="..\test\test250g.a">..\test\test250g.a</A>
- error: file inclusion within block expansion
- <A HREF="..\test\test250h.a">..\test\test250h.a</A>
- warn\error: correct filename reported for error


!! Self Inclusion
- <A HREF="..\test\test250i.a">..\test\test250i.a</A>
- warn: including self


!! File Label Scoping
- <A HREF="..\test\test251.a">..\test\test251.a</A>
- ok: local and variable labels
- <A HREF="..\test\test251e.a">..\test\test251e.a</A>
- error: global labels


!! Default Output File Names
- <A HREF="..\test\test252.a">..\test\test252.a</A>
- ok: default output file names set within include file
- <A HREF="..\test\test252e.a">..\test\test252e.a</A>
- warn: output filename same as input filename (output time)


!! Read Exclusion
- <A HREF="..\test\test253.a">..\test\test253.a</A>
- ok: "READONCE" psop
- <A HREF="..\test\test253b.a">..\test\test253b.a</A>
- ok: same base filename in another directory
- <A HREF="..\test\test253e.a">..\test\test253e.a</A>
- warn: circular inclusion (stacked inclusions)
- <A HREF="..\test\test253f.a">..\test\test253f.a</A>
- warning: circular inclusion (no stacked inclusions)
- <A HREF="..\test\test253g.a">..\test\test253g.a</A>
- warn: previous inclusion


!! Early Read Termination
- <A HREF="..\test\test255.a">..\test\test255.a</A>
- ok: "END" psop (w/o start address)
- <A HREF="..\test\test255b.a">..\test\test255b.a</A>
- ok: "END" psop (w/ start address)
- <A HREF="..\test\test255e.a">..\test\test255e.a</A>
- warn: "END" psop in include files (w/ + w/o start address)
- <A HREF="..\test\test255f.a">..\test\test255f.a</A>
- warn\error\fatal: "END" psop in macro expansion (w/o start address)
- <A HREF="..\test\test255g.a">..\test\test255g.a</A>
- warn\error\fatal: "END" psop in macro expansion (w/ start address)
- <A HREF="..\test\test255h.a">..\test\test255h.a</A>
- warn\error\fatal: "END" psop in "IF" block (w/o start address)
- <A HREF="..\test\test255i.a">..\test\test255i.a</A>
- warn\error\fatal: "END" psop in "IF" block (w/ start address)


!! Include File as Last Line of Root File
- <A HREF="..\test\test257.a">..\test\test257.a</A>
- ok: file inclusion; no END psop in any file


! Binary File Inclusion


!! Binary Inclusion
- <A HREF="..\test\test260.a">..\test\test260.a</A>
- ok: binary file inclusion
- <A HREF="..\test\test260e.a">..\test\test260e.a</A>
- warn\error: malformed "INCBIN"
- <A HREF="..\test\test260f.a">..\test\test260f.a</A>
- warn: odd argument values


! Motorola SRecord Object


!! Basic Records
- <A HREF="..\test\test280.a">..\test\test280.a</A>
- ok: 16-bit (header, data, count and EOF records)
- <A HREF="..\test\test280b.a">..\test\test280b.a</A>
- ok: 24-bit (header, data, count and EOF records)
- <A HREF="..\test\test280c.a">..\test\test280c.a</A>
- ok: 32-bit (header, data, count and EOF records)


!! Start Records
- <A HREF="..\test\test281.a">..\test\test281.a</A>
- ok: 16-bit (header, data, count and non-zero EOF records)
- <A HREF="..\test\test281b.a">..\test\test281b.a</A>
- ok: 24-bit (header, data, count and non-zero EOF records)
- <A HREF="..\test\test281c.a">..\test\test281c.a</A>
- ok: 32-bit (header, data, count and non-zero EOF records)
- <A HREF="..\test\test281e.a">..\test\test281e.a</A>
- error: start address out of range (16-bit)
- <A HREF="..\test\test281f.a">..\test\test281f.a</A>
- error: start address out of range (24-bit)
- <A HREF="..\test\test281g.a">..\test\test281g.a</A>
- error: start address out of range (32-bit)
- <A HREF="..\test\test281h.a">..\test\test281h.a</A>
- error: start address not numeric
- <A HREF="..\test\test281i.a">..\test\test281i.a</A>
- error: start address not found
- <A HREF="..\test\test281j.a">..\test\test281j.a</A>
- error: "END" w/ start expression within macro (unresolvable)


!! Assume Wider Address Type
- <A HREF="..\test\test282.a">..\test\test282.a</A>
- ok: 16-bit to 24-bit
- <A HREF="..\test\test282b.a">..\test\test282b.a</A>
- ok: 16-bit to 32-bit
- <A HREF="..\test\test282c.a">..\test\test282c.a</A>
- ok: 24-bit to 32-bit
- <A HREF="..\test\test282e.a">..\test\test282e.a</A>
- warn: unrecognized assumption
- <A HREF="..\test\test282f.a">..\test\test282f.a</A>
- warn: 16 bit to 24 bits, cannot change
- <A HREF="..\test\test282g.a">..\test\test282g.a</A>
- warn: 16 bit to 32 bits, cannot change
- <A HREF="..\test\test282h.a">..\test\test282h.a</A>
- warn: 24 bit to 32 bits, cannot change
- <A HREF="..\test\test282i.a">..\test\test282i.a</A>
- error: 16 bit to 24 bits, bad start address
- <A HREF="..\test\test282j.a">..\test\test282j.a</A>
- error: 16 bit to 32 bits, bad start address
- <A HREF="..\test\test282k.a">..\test\test282k.a</A>
- error: 24 bit to 32 bits, bad start address
- <A HREF="..\test\test282l.a">..\test\test282l.a</A>
- error: 16 bit to 24 bits, bad data address


!! Assume Narrower Address Type
- <A HREF="..\test\test283.a">..\test\test283.a</A>
- ok: 32-bit to 24-bit
- <A HREF="..\test\test283b.a">..\test\test283b.a</A>
- ok: 32-bit to 16-bit
- <A HREF="..\test\test283c.a">..\test\test283c.a</A>
- ok: 24-bit to 16-bit
- <A HREF="..\test\test283e.a">..\test\test283e.a</A>
- error: 32-bit to 24-bit, bad start address
- <A HREF="..\test\test283f.a">..\test\test283f.a</A>
- error: 32-bit to 24-bit, bad data address (early assumption)
- <A HREF="..\test\test283g.a">..\test\test283g.a</A>
- error: 32-bit to 24-bit, bad data address (late assumption)


!! Named Output File
- <A HREF="..\test\test284.a">..\test\test284.a</A>
- ok: user-specified name
- <A HREF="..\test\test284e.a">..\test\test284e.a</A>
- warn\error: malformed name
- <A HREF="..\test\test284f.a">..\test\test284f.a</A>
- warn: cannot change name once set


!! Assume Record Supressed
- <A HREF="..\test\test285.a">..\test\test285.a</A>
- ok: assume no S0 (header) record (16-bit)
- <A HREF="..\test\test285b.a">..\test\test285b.a</A>
- ok: assume no S5/S6 (count) record (16-bit)
- <A HREF="..\test\test285c.a">..\test\test285c.a</A>
- ok: assume no header or count (16-bit)
- <A HREF="..\test\test285d.a">..\test\test285d.a</A>
- ok: assume no name in header (16-bit)


!! Assume More Data
- <A HREF="..\test\test286.a">..\test\test286.a</A>
- ok: assume 32 hex data bytes per record (16-bit)
- <A HREF="..\test\test286b.a">..\test\test286b.a</A>
- ok: assume 32 hex data bytes per record (24-bit)
- <A HREF="..\test\test286c.a">..\test\test286c.a</A>
- ok: assume 32 hex data bytes per record (32-bit)
- <A HREF="..\test\test286e.a">..\test\test286e.a</A>
- warn\error: malformed; out-of-range; unique value


!! Overlapping Addresses (Monolithic)
- <A HREF="..\test\test287.a">..\test\test287.a</A>
- ok: 16-bit (header, data, count and EOF records)
- <A HREF="..\test\test287b.a">..\test\test287b.a</A>
- ok: 24-bit (header, data, count and EOF records)
- <A HREF="..\test\test287c.a">..\test\test287c.a</A>
- ok: 32-bit (header, data, count and EOF records)


! Intel Hexadecimal Object


!! Basic Records
- <A HREF="..\test\test290.a">..\test\test290.a</A>
- ok: 16-bit (data and EOF records)
- <A HREF="..\test\test290b.a">..\test\test290b.a</A>
- ok: 20-bit (data, EOF and extended segment address records)
- <A HREF="..\test\test290c.a">..\test\test290c.a</A>
- ok: 32-bit (data, EOF and extended linear address records)


!! Start Records
- <A HREF="..\test\test291.a">..\test\test291.a</A>
- ok: 16-bit (data and EOF records)
- <A HREF="..\test\test291b.a">..\test\test291b.a</A>
- ok: 20-bit (data, EOF, extended and start segment address records)
- <A HREF="..\test\test291c.a">..\test\test291c.a</A>
- ok: 32-bit (data, EOF, extended and start linear address records)
- <A HREF="..\test\test291e.a">..\test\test291e.a</A>
- error: start address out of range (16-bit)
- <A HREF="..\test\test291f.a">..\test\test291f.a</A>
- error: start address out of range (20-bit)
- <A HREF="..\test\test291g.a">..\test\test291g.a</A>
- error: start address out of range (32-bit)
- <A HREF="..\test\test291h.a">..\test\test291h.a</A>
- error: start address not numeric
- <A HREF="..\test\test291i.a">..\test\test291i.a</A>
- error: start address not found
- <A HREF="..\test\test291j.a">..\test\test291j.a</A>
- error: "END" w/ start expression within macro


!! Assume Wider Address Type
- <A HREF="..\test\test292.a">..\test\test292.a</A>
- ok: 16-bit to 20-bit
- <A HREF="..\test\test292b.a">..\test\test292b.a</A>
- ok: 16-bit to 32-bit
- <A HREF="..\test\test292c.a">..\test\test292c.a</A>
- ok: 20-bit to 32-bit
- <A HREF="..\test\test292e.a">..\test\test292e.a</A>
- warn: unrecognized assumption
- <A HREF="..\test\test292f.a">..\test\test292f.a</A>
- warn: 16 bits to 20 bits, cannot change
- <A HREF="..\test\test292g.a">..\test\test292g.a</A>
- warn: 16 bits to 32 bits, cannot change
- <A HREF="..\test\test292h.a">..\test\test292h.a</A>
- error: 20 bits to 32 bits; cannot change
- <A HREF="..\test\test292i.a">..\test\test292i.a</A>
- error: 16 bits to 20 bits; bad start address
- <A HREF="..\test\test292j.a">..\test\test292j.a</A>
- error: 16 bits to 32 bits; bad start address
- <A HREF="..\test\test292k.a">..\test\test292k.a</A>
- error: 20 bits to 32 bits; bad start address
- <A HREF="..\test\test292l.a">..\test\test292l.a</A>
- error: 16 bits to 20 bits; bad data address
- <A HREF="..\test\test292m.a">..\test\test292m.a</A>
- error: 20 bits to 32 bits; bad data address


!! Assume Narrower Address Type
- <A HREF="..\test\test293.a">..\test\test293.a</A>
- ok: 32-bit to 20-bit
- <A HREF="..\test\test293b.a">..\test\test293b.a</A>
- ok: 32-bit to 16-bit
- <A HREF="..\test\test293c.a">..\test\test293c.a</A>
- ok: 20-bit to 16-bit
- <A HREF="..\test\test293e.a">..\test\test293e.a</A>
- error: 32 bits to 20 bits; bad start address
- <A HREF="..\test\test293f.a">..\test\test293f.a</A>
- error: 32 bits to 20 bits; bad data address (early assumption)
- <A HREF="..\test\test293g.a">..\test\test293g.a</A>
- error: 32 bits to 20 bits; bad data address (late assumption)


!! Named Output File
- <A HREF="..\test\test294.a">..\test\test294.a</A>
- ok: user-specified name
- <A HREF="..\test\test294e.a">..\test\test294e.a</A>
- warn\error: malformed name
- <A HREF="..\test\test294f.a">..\test\test294f.a</A>
- warn: cannot change name once set


!! Output Greater than 64K
- <A HREF="..\test\test295.a">..\test\test295.a</A>
- ok: 20-bit (data, EOF and extended segment address records)
- <A HREF="..\test\test295b.a">..\test\test295b.a</A>
- ok: 32-bit (data, EOF and extended segment address records)
- <A HREF="..\test\test295e.a">..\test\test295e.a</A>
- fatal: 16-bit


!! Assume More Data
- <A HREF="..\test\test296.a">..\test\test296.a</A>
- ok: assume 32 hex data bytes per record (16-bit)
- <A HREF="..\test\test296b.a">..\test\test296b.a</A>
- ok: assume 32 hex data bytes per record (20-bit)
- <A HREF="..\test\test296c.a">..\test\test296c.a</A>
- ok: assume 32 hex data bytes per record (32-bit)


!! Overlapping Addresses (Monolithic)
- <A HREF="..\test\test297.a">..\test\test297.a</A>
- ok: 16-bit (data and EOF records)
- <A HREF="..\test\test297b.a">..\test\test297b.a</A>
- ok:20-bit (data and EOF records)
- <A HREF="..\test\test297c.a">..\test\test297c.a</A>
- ok:32-bit (data and EOF records)


!! Address Jumps Force New Address Records
- <A HREF="..\test\test298.a">..\test\test298.a</A>
- ok: 20-bit (data, EOF and extended segment address records)
- <A HREF="..\test\test298b.a">..\test\test298b.a</A>
- ok: 32-bit (data, EOF and extended segment address records)
- <A HREF="..\test\test298c.a">..\test\test298c.a</A>
- ok: 16-bit (data records)


! Segments


!! Basic Definition
- <A HREF="..\test\test300.a">..\test\test300.a</A>
- ok: correct addresses of relative segment data (16-bit)
- <A HREF="..\test\test300b.a">..\test\test300b.a</A>
- ok: correct addresses of relative segment data (24-bit)
- <A HREF="..\test\test300c.a">..\test\test300c.a</A>
- ok: correct addresses of relative segment data (32-bit)
- <A HREF="..\test\test300d.a">..\test\test300d.a</A>
- ok: prevent segment map from listing
- <A HREF="..\test\test300e.a">..\test\test300e.a</A>
- error: bad segment names and unmatched block
- <A HREF="..\test\test300f.a">..\test\test300f.a</A>
- fatal: SEGMENT after first ORG outside of segment (therefore monolithic)
- <A HREF="..\test\test300g.a">..\test\test300g.a</A>
- error: mis-matched segment names
- <A HREF="..\test\test300h.a">..\test\test300h.a</A>
- error: no absolute segment
- <A HREF="..\test\test300i.a">..\test\test300i.a</A>
- error\fatal: ORG outside of any segment
- <A HREF="..\test\test300j.a">..\test\test300j.a</A>
- error: repeat ORGs of one segment must have same value
- <A HREF="..\test\test300k.a">..\test\test300k.a</A>
- error\fatal: 16-bit relative segment exceeds max pc value (at fixup)
- <A HREF="..\test\test300l.a">..\test\test300l.a</A>
- error\fatal: 24-bit relative segment exceeds max pc value (at fixup)
- <A HREF="..\test\test300m.a">..\test\test300m.a</A>
- error\fatal: 32-bit relative segment exceeds max pc value (at fixup)
- <A HREF="..\test\test300n.a">..\test\test300n.a</A>
- error\fatal: 16-bit relative segment exceeds max pc value (during assembly)
- <A HREF="..\test\test300o.a">..\test\test300o.a</A>
- error\fatal: 24-bit relative segment exceeds max pc value (during assembly)
- <A HREF="..\test\test300p.a">..\test\test300p.a</A>
- error\fatal: 32-bit relative segment exceeds max pc value (during assembly)
- <A HREF="..\test\test300q.a">..\test\test300q.a</A>
- error\fatal: too many segments (Monolithic, by ORG)
- <A HREF="..\test\test300r.a">..\test\test300r.a</A>
- error\fatal: too many segments (Monolithic, by DS)
- <A HREF="..\test\test300s.a">..\test\test300s.a</A>
- error: segment ORG must come before data storage
- <A HREF="..\test\test300t.a">..\test\test300t.a</A>
- error: crossed block structures in segment fragments
- <A HREF="..\test\test300u.a">..\test\test300u.a</A>
- error\fatal: data storage outside of any segment
- <A HREF="..\test\test300v.a">..\test\test300v.a</A>
- error\fatal: DS outside of any segment
- <A HREF="..\test\test300w.a">..\test\test300w.a</A>
- error\fatal: implicit label value assignment outside of any segment
- <A HREF="..\test\test300x.a">..\test\test300x.a</A>
- error\fatal: program counter in expression outside of any segment


!! Segments Re-Used
- <A HREF="..\test\test301.a">..\test\test301.a</A>
- ok: correct addresses of absolute and relative data (16-bit)
- <A HREF="..\test\test301b.a">..\test\test301b.a</A>
- ok: correct addresses of absolute and relative data (24-bit)
- <A HREF="..\test\test301c.a">..\test\test301c.a</A>
- ok: correct addresses of absolute and relative data (32-bit)
- <A HREF="..\test\test301e.a">..\test\test301e.a</A>
- error\fatal: 16-bit relative segment exceeds max pc value (at fixup)
- <A HREF="..\test\test301f.a">..\test\test301f.a</A>
- error\fatal: 24-bit relative segment exceeds max pc value (at fixup)
- <A HREF="..\test\test301g.a">..\test\test301g.a</A>
- error\fatal: 32-bit relative segment exceeds max pc value (at fixup)


!! Legal Data Storage
- <A HREF="..\test\test302.a">..\test\test302.a</A>
- ok: first named segment must be absolute before end of source
- <A HREF="..\test\test302e.a">..\test\test302e.a</A>
- error: first named segment must be absolute before end of source
- <A HREF="..\test\test302f.a">..\test\test302f.a</A>
- error: storing data in first segment before making it absolute
- <A HREF="..\test\test302g.a">..\test\test302g.a</A>
- error\fatal: cannot store data outside of any segment


!! Labels
- <A HREF="..\test\test303.a">..\test\test303.a</A>
- ok: implicit assignment of program counter to numeric labels
- <A HREF="..\test\test303b.a">..\test\test303b.a</A>
- ok: implicit assignment of program counter to string labels
- <A HREF="..\test\test303e.a">..\test\test303e.a</A>
- error: missing global labels
- <A HREF="..\test\test303f.a">..\test\test303f.a</A>
- error: reference to locals in other segments
- <A HREF="..\test\test303g.a">..\test\test303g.a</A>
- warn: forward reference to variable label


!! Program Counter (Implicit)
- <A HREF="..\test\test304.a">..\test\test304.a</A>
- ok: implicit use of program counter (relative offsets)
- <A HREF="..\test\test304e.a">..\test\test304e.a</A>
- fatal: pc invalid outside segments
- <A HREF="..\test\test304f.a">..\test\test304f.a</A>
- warn\error\fatal: "DS" psop with negative values (relative segment)
- <A HREF="..\test\test304g.a">..\test\test304g.a</A>
- fatal: "END" psop cannot be labeled
- <A HREF="..\test\test304h.a">..\test\test304h.a</A>
- error: cannot make absolute ( so cannot resolve data )
- <A HREF="..\test\test304i.a">..\test\test304i.a</A>
- warn/error/fatal: "END" psop cannot be used inside segment (unlabeled, no start address)
- <A HREF="..\test\test304j.a">..\test\test304j.a</A>
- warn/error/fatal: "END" psop cannot be used inside segment (labeled, with start address)


!! Program Counter (Explicit)
- <A HREF="..\test\test305.a">..\test\test305.a</A>
- ok: PC expressions in relative segments
- <A HREF="..\test\test305e.a">..\test\test305e.a</A>
- error: illegal forward reference to pc in relative segment


!! "USESEGMENTS" psop
- <A HREF="..\test\test306.a">..\test\test306.a</A>
- ok: explicit declaration of segment use
- <A HREF="..\test\test306b.a">..\test\test306b.a</A>
- ok: explicit declaration of segment use (first use inside segment)
- <A HREF="..\test\test306e.a">..\test\test306e.a</A>
- fatal: explicit declaration of segment use after "ORG" used


!! Segment Count
- <A HREF="..\test\test307e.a">..\test\test307e.a</A>
- fatal: too many segments


!! Intel Hexfile Output (Single File)
- <A HREF="..\test\test310.a">..\test\test310.a</A>
- ok: correct output sequence and start address (16-bit)
- <A HREF="..\test\test310b.a">..\test\test310b.a</A>
- ok: correct output sequence and start address (20-bit)
- <A HREF="..\test\test310c.a">..\test\test310c.a</A>
- ok: correct output sequence and start address (32-bit)


!! Intel Hexfile Output (By Segments, Default Names)
- <A HREF="..\test\test311.a">..\test\test311.a</A>
- ok: correct output sequence and start address (16-bit)
- <A HREF="..\test\test311b.a">..\test\test311b.a</A>
- ok: correct output sequence and start address (20-bit)
- <A HREF="..\test\test311c.a">..\test\test311c.a</A>
- ok: correct output sequence and start address (32-bit)


!! Intel Hexfile Output (By Segments, "###" Template)
- <A HREF="..\test\test312.a">..\test\test312.a</A>
- ok: correct output sequence and start address (16-bit)
- <A HREF="..\test\test312b.a">..\test\test312b.a</A>
- ok: correct output sequence and start address (20-bit)
- <A HREF="..\test\test312c.a">..\test\test312c.a</A>
- ok: correct output sequence and start address (32-bit)
- <A HREF="..\test\test312e.a">..\test\test312e.a</A>
- error: bad template names


!! Intel Hexfile Output (By Segment)
- <A HREF="..\test\test313.a">..\test\test313.a</A>
- ok: non-segmented program produces no output (16-bit)


!! Intel Hexfile Output (By Blocks, Default Names)
- <A HREF="..\test\test315.a">..\test\test315.a</A>
- ok: correct output sequence and start address (16-bit)
- <A HREF="..\test\test315b.a">..\test\test315b.a</A>
- ok: correct output sequence and start address (20-bit)
- <A HREF="..\test\test315c.a">..\test\test315c.a</A>
- ok: correct output sequence and start address (32-bit)


!! Intel Hexfile Output (By Blocks, ".###" Template)
- <A HREF="..\test\test316.a">..\test\test316.a</A>
- ok: correct output sequence and start address (16-bit)
- <A HREF="..\test\test316b.a">..\test\test316b.a</A>
- ok: correct output sequence and start address (20-bit)
- <A HREF="..\test\test316c.a">..\test\test316c.a</A>
- ok: correct output sequence and start address (32-bit)


!! Intel Hexfile Output (By Blocks, Overlapping)
- <A HREF="..\test\test317.a">..\test\test317.a</A>
- ok: correct output sequence and start address (16-bit)
- <A HREF="..\test\test317b.a">..\test\test317b.a</A>
- ok: correct output sequence and start address (20-bit)
- <A HREF="..\test\test317c.a">..\test\test317c.a</A>
- ok: correct output sequence and start address (32-bit)


!! Motorola Hexfile Output (Single File)
- <A HREF="..\test\test320.a">..\test\test320.a</A>
- ok: correct output sequence and start address (16-bit)
- <A HREF="..\test\test320b.a">..\test\test320b.a</A>
- ok: correct output sequence and start address (24-bit)
- <A HREF="..\test\test320c.a">..\test\test320c.a</A>
- ok: correct output sequence and start address (32-bit)


!! Motorola Hexfile Output (By Segments, Default Names)
- <A HREF="..\test\test321.a">..\test\test321.a</A>
- ok: correct output sequence and start address (16-bit)
- <A HREF="..\test\test321b.a">..\test\test321b.a</A>
- ok: correct output sequence and start address (24-bit)
- <A HREF="..\test\test321c.a">..\test\test321c.a</A>
- ok: correct output sequence and start address (32-bit)


!! Motorola Hexfile Output (By Segments, "###." Template)
- <A HREF="..\test\test322.a">..\test\test322.a</A>
- ok: correct output sequence and start address (16-bit)
- <A HREF="..\test\test322b.a">..\test\test322b.a</A>
- ok: correct output sequence and start address (24-bit)
- <A HREF="..\test\test322c.a">..\test\test322c.a</A>
- ok: correct output sequence and start address (32-bit)


!! Motorola Hexfile Output (Default Names, No Header)
- <A HREF="..\test\test323.a">..\test\test323.a</A>
- ok: correct output sequence and start address (16-bit)
- <A HREF="..\test\test323b.a">..\test\test323b.a</A>
- ok: correct output sequence and start address (16-bit)
- <A HREF="..\test\test323c.a">..\test\test323c.a</A>
- ok: correct output sequence and start address (16-bit)


!! Motorola Hexfile Output (By Blocks, Default Names)
- <A HREF="..\test\test325.a">..\test\test325.a</A>
- ok: correct output sequence and start address (16-bit)
- <A HREF="..\test\test325b.a">..\test\test325b.a</A>
- ok: correct output sequence and start address (24-bit)
- <A HREF="..\test\test325c.a">..\test\test325c.a</A>
- ok: correct output sequence and start address (32-bit)


!! Motorola Hexfile Output (By Blocks, ".###" Template)
- <A HREF="..\test\test326.a">..\test\test326.a</A>
- ok: correct output sequence and start address (16-bit)
- <A HREF="..\test\test326b.a">..\test\test326b.a</A>
- ok: correct output sequence and start address (24-bit)
- <A HREF="..\test\test326c.a">..\test\test326c.a</A>
- ok: correct output sequence and start address (32-bit)


!! Object Output (By Segments, Default Names)
- <A HREF="..\test\test331.a">..\test\test331.a</A>
- ok: 16-bit


!! Object Output (By Segments, "####." Template)
- <A HREF="..\test\test332.a">..\test\test332.a</A>
- ok: 16-bit


!! Object Output (By Blocks, Default Names)
- <A HREF="..\test\test335.a">..\test\test335.a</A>
- ok: 16-bit


!! Object Output (By Blocks, ".###" Template)
- <A HREF="..\test\test336.a">..\test\test336.a</A>
- ok: 16-bit


!! Raw Hex Output (By Segments, Default Names)
- <A HREF="..\test\test341.a">..\test\test341.a</A>
- ok: 16-bit


!! Raw Hex Output (By Segments, "##." Template)
- <A HREF="..\test\test342.a">..\test\test342.a</A>
- ok: 16-bit


!! Raw Hex Output (By Blocks, Default Names)
- <A HREF="..\test\test345.a">..\test\test345.a</A>
- ok: 16-bit


!! Raw Hex Output (By Blocks, ".###" Template)
- <A HREF="..\test\test346.a">..\test\test346.a</A>
- ok: 16-bit


!! Uninitialized Segments
- <A HREF="..\test\test350.a">..\test\test350.a</A>
- ok: basic definition
- <A HREF="..\test\test350b.a">..\test\test350b.a</A>
- ok: basic definition
- <A HREF="..\test\test350c.a">..\test\test350c.a</A>
- ok: basic definition
- <A HREF="..\test\test350d.a">..\test\test350d.a</A>
- ok: basic definition
- <A HREF="..\test\test350e.a">..\test\test350e.a</A>
- warn\error\fatal: declaration errors
- <A HREF="..\test\test350f.a">..\test\test350f.a</A>
- fatal: cannot store data in "uninitialized" segments
- <A HREF="..\test\test350g.a">..\test\test350g.a</A>
- error: no "uninitialized" after "padto"
- <A HREF="..\test\test350h.a">..\test\test350h.a</A>
- error: no "padto" after "uninitialized"
- <A HREF="..\test\test350i.a">..\test\test350i.a</A>
- fatal: can't use in monolithic program


!! Common Segments
- <A HREF="..\test\test352.a">..\test\test352.a</A>
- ok: basic definition
- <A HREF="..\test\test352b.a">..\test\test352b.a</A>
- ok: basic definition (absolute segments are absend)
- <A HREF="..\test\test352e.a">..\test\test352e.a</A>
- warn\error\fatal: declaration errors
- <A HREF="..\test\test352f.a">..\test\test352f.a</A>
- fatal: cannot store data in "common" segments
- <A HREF="..\test\test352g.a">..\test\test352g.a</A>
- error: no COMMON with PADTO or PADFROM
- <A HREF="..\test\test352h.a">..\test\test352h.a</A>
- fatal: can't use in monolithic program


!! "RELORG" Pseudo Op
- <A HREF="..\test\test354.a">..\test\test354.a</A>
- ok: correct addresses of relative segment data (16-bit)
- <A HREF="..\test\test354b.a">..\test\test354b.a</A>
- ok: correct addresses of relative segment data (24-bit)
- <A HREF="..\test\test354c.a">..\test\test354c.a</A>
- ok: correct addresses of relative segment data (32-bit)
- <A HREF="..\test\test354d.a">..\test\test354d.a</A>
- ok: "RELORG" can follow segment types
- <A HREF="..\test\test354e.a">..\test\test354e.a</A>
- error: segments cannot be re-typed
- <A HREF="..\test\test354f.a">..\test\test354f.a</A>
- warn: labels and expressions
- <A HREF="..\test\test354g.a">..\test\test354g.a</A>
- error\fatal: outside segment


!! "ABSEND" and "RELEND" Pseudo Ops
- <A HREF="..\test\test356.a">..\test\test356.a</A>
- ok: correct addresses of relative segment data (16-bit)
- <A HREF="..\test\test356b.a">..\test\test356b.a</A>
- ok: correct addresses of relative segment data (24-bit)
- <A HREF="..\test\test356c.a">..\test\test356c.a</A>
- ok: correct addresses of relative segment data (32-bit)
- <A HREF="..\test\test356d.a">..\test\test356d.a</A>
- ok: segment types "RELEND" can preceed
- <A HREF="..\test\test356e.a">..\test\test356e.a</A>
- error: segments cannot be re-typed
- <A HREF="..\test\test356f.a">..\test\test356f.a</A>
- warn\error: labels and expressions
- <A HREF="..\test\test356g.a">..\test\test356g.a</A>
- error\fatal: ABSEND outside segment
- <A HREF="..\test\test356h.a">..\test\test356h.a</A>
- error\fatal: RELEND outside segment
- <A HREF="..\test\test356i.a">..\test\test356i.a</A>
- error: cannot make segments absolute
- <A HREF="..\test\test356j.a">..\test\test356j.a</A>
- error: RELEND cannot be last segment
- <A HREF="..\test\test356k.a">..\test\test356k.a</A>
- error: program counter pushed below zero


!! Segment Map Identification
- <A HREF="..\test\test360.a">..\test\test360.a</A>
- ok: correct identification of segment type


!! Nested Segments
- <A HREF="..\test\test370.a">..\test\test370.a</A>
- ok: correct addresses of segment data (16-bit)
- <A HREF="..\test\test370b.a">..\test\test370b.a</A>
- ok: correct addresses of segment data (24-bit)
- <A HREF="..\test\test370c.a">..\test\test370c.a</A>
- ok: correct addresses of segment data (32-bit)
- <A HREF="..\test\test370e.a">..\test\test370e.a</A>
- error: segment without endsegment (outer, named)
- <A HREF="..\test\test370f.a">..\test\test370f.a</A>
- error: segment without endsegment (inner, named)
- <A HREF="..\test\test370g.a">..\test\test370g.a</A>
- error: segment without endsegment (unnamed)
- <A HREF="..\test\test370h.a">..\test\test370h.a</A>
- error: endsegment without segment
- <A HREF="..\test\test370i.a">..\test\test370i.a</A>
- error: self-nesting exceeds max depth
- <A HREF="..\test\test370j.a">..\test\test370j.a</A>
- error: nested segments have nested local scopes


! Program Counter Manipulation


!! Define Uninitialized Storage
- <A HREF="..\test\test400.a">..\test\test400.a</A>
- ok: "DS" psop (monolithic)
- <A HREF="..\test\test400b.a">..\test\test400b.a</A>
- ok: "DS" psop (segmented)
- <A HREF="..\test\test400e.a">..\test\test400e.a</A>
- error: malformed "DS" psop
- <A HREF="..\test\test400f.a">..\test\test400f.a</A>
- warn/error: negative "DS" psop useage
- <A HREF="..\test\test400g.a">..\test\test400g.a</A>
- error: 16-bit program counter out of range (negative)
- <A HREF="..\test\test400h.a">..\test\test400h.a</A>
- error: 16-bit program counter out of range (too big)
- <A HREF="..\test\test400i.a">..\test\test400i.a</A>
- error: 24-bit program counter out of range (negative)
- <A HREF="..\test\test400j.a">..\test\test400j.a</A>
- error: 24-bit program counter out of range (too big)
- <A HREF="..\test\test400k.a">..\test\test400k.a</A>
- error: 32-bit program counter out of range (negative)
- <A HREF="..\test\test400l.a">..\test\test400l.a</A>
- error: 32-bit program counter out of range (too big)
- <A HREF="..\test\test400m.a">..\test\test400m.a</A>
- error: uninitialized program counter
- <A HREF="..\test\test400n.a">..\test\test400n.a</A>
- error\fatal: DS outside of any segment (explicit segments)
- <A HREF="..\test\test400o.a">..\test\test400o.a</A>
- error\fatal: negative DS (explicit segments)
- <A HREF="..\test\test400p.a">..\test\test400p.a</A>
- error\fatal: negative DS outside segment (explicit segments)
- <A HREF="..\test\test400q.a">..\test\test400q.a</A>
- fatal: cannot store data in uninitialized segment
- <A HREF="..\test\test400r.a">..\test\test400r.a</A>
- fatal: cannot use DS in data segment


!! Fill Block With Constant Data
- <A HREF="..\test\test402.a">..\test\test402.a</A>
- ok: "FILL" psop
- <A HREF="..\test\test402e.a">..\test\test402e.a</A>
- error: malformed "FILL" psop
- <A HREF="..\test\test402f.a">..\test\test402f.a</A>
- warn\error fatal: negative fill value
- <A HREF="..\test\test402g.a">..\test\test402g.a</A>
- error\fatal: uninitialized program counter
- <A HREF="..\test\test402h.a">..\test\test402h.a</A>
- error\fatal: FILL outside of any segment (explicit segments)
- <A HREF="..\test\test402i.a">..\test\test402i.a</A>
- error\fatal: 16-bit program counter pushed out of range (too big)
- <A HREF="..\test\test402j.a">..\test\test402j.a</A>
- error\fatal: 24-bit program counter pushed out of range (too big)
- <A HREF="..\test\test402k.a">..\test\test402k.a</A>
- error\fatal: 32-bit program counter pushed out of range (too big)
- <A HREF="..\test\test402l.a">..\test\test402l.a</A>
- fatal: cannot use FILL in uninitialized segment
- <A HREF="..\test\test402m.a">..\test\test402m.a</A>
- error\fatal: segmented 16-bit pc pushed out of range (too small)
- <A HREF="..\test\test402n.a">..\test\test402n.a</A>
- error\fatal: segmented 16-bit pc pushed out of range (too big)
- <A HREF="..\test\test402o.a">..\test\test402o.a</A>
- error\fatal: segmented 16-bit pc pushed out of range (too big)
- <A HREF="..\test\test402p.a">..\test\test402p.a</A>
- error\fatal: segmented 16-bit pc pushed out of range (too big)
- <A HREF="..\test\test402q.a">..\test\test402q.a</A>
- error\fatal: fill out of cpu range
- <A HREF="..\test\test402r.a">..\test\test402r.a</A>
- warn: odd label useage


!! Pad To Specific Byte Boundary
- <A HREF="..\test\test404.a">..\test\test404.a</A>
- ok: "PADTO" pseudo op (monolithic)
- <A HREF="..\test\test404b.a">..\test\test404b.a</A>
- ok: "PADTO" pseudo op (segmented)
- <A HREF="..\test\test404c.a">..\test\test404c.a</A>
- ok: "PADTO" pseudo op (segmented; padding not listed)
- <A HREF="..\test\test404d.a">..\test\test404d.a</A>
- ok: "PADTO" pseudo op
- <A HREF="..\test\test404e.a">..\test\test404e.a</A>
- warn\error\fatal: boundary value out of range
- <A HREF="..\test\test404f.a">..\test\test404f.a</A>
- warn: incompatible segment types
- <A HREF="..\test\test404g.a">..\test\test404g.a</A>
- error\fatal: program counter forced out of range (implicit segments)
- <A HREF="..\test\test404h.a">..\test\test404h.a</A>
- error\fatal: program counter forced out of range (explicit segments)
- <A HREF="..\test\test404i.a">..\test\test404i.a</A>
- warn: cannot change pad value once set
- <A HREF="..\test\test404j.a">..\test\test404j.a</A>
- error\fatal: PADTO before CPU set (monolithic)
- <A HREF="..\test\test404k.a">..\test\test404k.a</A>
- error\fatal: PADTO before first ORG (monolithic)
- <A HREF="..\test\test404l.a">..\test\test404l.a</A>
- error\fatal: PADTO outside of any segment (explicit segments)
- <A HREF="..\test\test404m.a">..\test\test404m.a</A>
- error: PADTO cannot follow relative end segment
- <A HREF="..\test\test404n.a">..\test\test404n.a</A>
- error: PADTO cannot follow pad from segment


!! Pad From Specific Byte Boundary
- <A HREF="..\test\test406.a">..\test\test406.a</A>
- ok: "PADFROM" pseudo op (segmented)
- <A HREF="..\test\test406b.a">..\test\test406b.a</A>
- ok: "PADFROM" pseudo op (segmented)
- <A HREF="..\test\test406c.a">..\test\test406c.a</A>
- ok: "PADFROM" pseudo op (segmented)
- <A HREF="..\test\test406d.a">..\test\test406d.a</A>
- ok: "PADFROM" pseudo op (segmented)
- <A HREF="..\test\test406e.a">..\test\test406e.a</A>
- warn\error: "PADFROM" not legal in monolithic programs
- <A HREF="..\test\test406f.a">..\test\test406f.a</A>
- warn: incompatible segment types
- <A HREF="..\test\test406g.a">..\test\test406g.a</A>
- error\fatal: program counter forced out of range (implicit segments)
- <A HREF="..\test\test406h.a">..\test\test406h.a</A>
- warn\error\fatal: program counter forced out of range (explicit segments)
- <A HREF="..\test\test406i.a">..\test\test406i.a</A>
- warn\error: cannot change pad value once set
- <A HREF="..\test\test406j.a">..\test\test406j.a</A>
- error\fatal: PADFROM before CPU set (monolithic)
- <A HREF="..\test\test406k.a">..\test\test406k.a</A>
- fatal: PADFROM before first ORG (monolithic)
- <A HREF="..\test\test406l.a">..\test\test406l.a</A>
- error\fatal: PADFROM outside of any segment (explicit segments)
- <A HREF="..\test\test406m.a">..\test\test406m.a</A>
- error\fatal: cannot make absolute (explicit segments)
- <A HREF="..\test\test406n.a">..\test\test406n.a</A>
- error\fatal: cannot make absolute (explicit segments)


! Program Listing


!! Listing
- <A HREF="..\test\test450.a">..\test\test450.a</A>
- ok: "LIST--" psops for OBJECT section
- <A HREF="..\test\test450b.a">..\test\test450b.a</A>
- ok: "LIST--" psops for LABELS section
- <A HREF="..\test\test450e.a">..\test\test450e.a</A>
- warn: unrecognized LIST options


!! No Flags Specified
- <A HREF="..\test\test451.a">..\test\test451.a</A>
- ok: "LIST--" defaults


!! Long Lines (Wrapped)
- <A HREF="..\test\test452.a">..\test\test452.a</A>
- ok: source lines too long to list on one line


!! Long Lines (Truncated)
- <A HREF="..\test\test453.a">..\test\test453.a</A>
- ok: source lines too long to list on one line


!! Show Line Numbers
- <A HREF="..\test\test454.a">..\test\test454.a</A>
- ok: prefix line numbers to listing


!! Change Page Width
- <A HREF="..\test\test455.a">..\test\test455.a</A>
- ok: "PAGESIZE" psop (page width=132)
- <A HREF="..\test\test455b.a">..\test\test455b.a</A>
- ok: "PAGESIZE" psop (page width=250)
- <A HREF="..\test\test455c.a">..\test\test455c.a</A>
- ok: "PAGESIZE" psop (page width=50)
- <A HREF="..\test\test455d.a">..\test\test455d.a</A>
- ok: "PAGESIZE" psop (page width=0; no right edge)
- <A HREF="..\test\test455e.a">..\test\test455e.a</A>
- warn\error: bad values


!! Change Left Margin
- <A HREF="..\test\test457.a">..\test\test457.a</A>
- ok: "MARGIN" psop (left margin=2, w/o line numbers)
- <A HREF="..\test\test457b.a">..\test\test457b.a</A>
- ok: "MARGIN" psop (left margin=5, w/ line numbers)
- <A HREF="..\test\test457c.a">..\test\test457c.a</A>
- ok: push listing far to right
- <A HREF="..\test\test457e.a">..\test\test457e.a</A>
- warn\error: bad values
- <A HREF="..\test\test457f.a">..\test\test457f.a</A>
- warn\fatal: no printable width
- <A HREF="..\test\test457g.a">..\test\test457g.a</A>
- warn: no printable width (recovers by changing page size)


!! Pagination
- <A HREF="..\test\test459.a">..\test\test459.a</A>
- ok: "PAGESIZE" and "MARGIN" psops (w/o line numbers)
- <A HREF="..\test\test459b.a">..\test\test459b.a</A>
- ok: "PAGESIZE" and "MARGIN" psops (w/ line numbers)
- <A HREF="..\test\test459c.a">..\test\test459c.a</A>
- ok: "PAGESIZE" and "MARGIN" psops (3-line pages w/ line numbers)
- <A HREF="..\test\test459e.a">..\test\test459e.a</A>
- warn\fatal: "PAGESIZE" and "MARGIN" psops (no printable length)


!! Change Line Spacing
- <A HREF="..\test\test461.a">..\test\test461.a</A>
- ok: "LINESPACE" psop (w/o pagination)
- <A HREF="..\test\test461b.a">..\test\test461b.a</A>
- ok: "LINESPACE" psop (w/ pagination)
- <A HREF="..\test\test461c.a">..\test\test461c.a</A>
- ok: "LINESPACE" psop (each line on its own page)
- <A HREF="..\test\test461e.a">..\test\test461e.a</A>
- warn\error: bad values


!! Change Header
- <A HREF="..\test\test463.a">..\test\test463.a</A>
- ok: "TITLE" psop (w/ string expression)
- <A HREF="..\test\test463b.a">..\test\test463b.a</A>
- ok: "TITLE" psop (w/ optional non-string argument)
- <A HREF="..\test\test463c.a">..\test\test463c.a</A>
- ok: "TITLE" psop (w/ null expression)
- <A HREF="..\test\test463e.a">..\test\test463e.a</A>
- error: bad arguments
- <A HREF="..\test\test463f.a">..\test\test463f.a</A>
- warn: title is unique
- <A HREF="..\test\test463g.a">..\test\test463g.a</A>
- error: null title


!! Macro Cross-Reference
- <A HREF="..\test\test470.a">..\test\test470.a</A>
- ok: w/o line numbers (source x-ref only)
- <A HREF="..\test\test470b.a">..\test\test470b.a</A>
- ok: w line numbers (both source and listing x-ref)
- <A HREF="..\test\test470c.a">..\test\test470c.a</A>
- ok: source and listing x-ref; listed and un-listed macro expansions


!! Global Label Cross-Reference
- <A HREF="..\test\test472.a">..\test\test472.a</A>
- ok: w/o line numbers (source x-ref only)
- <A HREF="..\test\test472b.a">..\test\test472b.a</A>
- ok: w/ line numbers (both source and listing x-ref)


!! Formfeed
- <A HREF="..\test\test474.a">..\test\test474.a</A>
- ok: "PAGE" psop (10-line page)
- <A HREF="..\test\test474b.a">..\test\test474b.a</A>
- ok: "PAGE" psop (w/o pagination enabled)
- <A HREF="..\test\test474c.a">..\test\test474c.a</A>
- ok: "PAGE" psop (10-line page; no effect in unlisted section)


!! Cross-Reference
- <A HREF="..\test\test476.a">..\test\test476.a</A>
- ok: macros only, w/ line numbers
- <A HREF="..\test\test476b.a">..\test\test476b.a</A>
- ok: global labels only, w/ line numbers


!! Show Assembly Statistics
- <A HREF="..\test\test478.a">..\test\test478.a</A>
- ok: "STATS" listing option


! Functions


!! VER() and VER$()
- <A HREF="..\test\test500.a">..\test\test500.a</A>
- ok: HXA version number
- <A HREF="..\test\test500e.a">..\test\test500e.a</A>
- error: malformed
- <A HREF="..\test\test500f.a">..\test\test500f.a</A>
- error: not found
- <A HREF="..\test\test500g.a">..\test\test500g.a</A>
- error: not found


!! LEN()
- <A HREF="..\test\test502.a">..\test\test502.a</A>
- ok: string length
- <A HREF="..\test\test502e.a">..\test\test502e.a</A>
- error: mis-use
- <A HREF="..\test\test502f.a">..\test\test502f.a</A>
- error: reserved name
- <A HREF="..\test\test502g.a">..\test\test502g.a</A>
- error: bad call


!! INDEX()
- <A HREF="..\test\test504.a">..\test\test504.a</A>
- ok: substring position (from left)
- <A HREF="..\test\test504e.a">..\test\test504e.a</A>
- error: substring position
- <A HREF="..\test\test504f.a">..\test\test504f.a</A>
- error: reserved name
- <A HREF="..\test\test504g.a">..\test\test504g.a</A>
- error: bad call


!! MID$()
- <A HREF="..\test\test506.a">..\test\test506.a</A>
- ok: substring extraction (by numeric index)
- <A HREF="..\test\test506e.a">..\test\test506e.a</A>
- error: substring position
- <A HREF="..\test\test506f.a">..\test\test506f.a</A>
- error: reserved name
- <A HREF="..\test\test506g.a">..\test\test506g.a</A>
- error: bad call


!! VAL()
- <A HREF="..\test\test508.a">..\test\test508.a</A>
- ok: evaluate string expression as numeric
- <A HREF="..\test\test508e.a">..\test\test508e.a</A>
- error: illegal expressions
- <A HREF="..\test\test508f.a">..\test\test508f.a</A>
- error: out of range expressions
- <A HREF="..\test\test508g.a">..\test\test508g.a</A>
- error: unresolved


!! STR$()
- <A HREF="..\test\test510.a">..\test\test510.a</A>
- ok: evaluate numeric expression as string
- <A HREF="..\test\test510e.a">..\test\test510e.a</A>
- error: malformed and mis-applied
- <A HREF="..\test\test510f.a">..\test\test510f.a</A>
- error: forward reference in string context


!! INDEXR()
- <A HREF="..\test\test512.a">..\test\test512.a</A>
- ok: substring position (from right)


!! TOLOWER$() and TOUPPER$()
- <A HREF="..\test\test514.a">..\test\test514.a</A>
- ok: convert string case
- <A HREF="..\test\test514e.a">..\test\test514e.a</A>
- error: assign result to numeric label


!! FORWARD()
- <A HREF="..\test\test516.a">..\test\test516.a</A>
- ok: check expression for forward reference
- <A HREF="..\test\test516e.a">..\test\test516e.a</A>
- error: bad parse
- <A HREF="..\test\test516f.a">..\test\test516f.a</A>
- error: bad evaluation


!! CHR$() and ORD()
- <A HREF="..\test\test518.a">..\test\test518.a</A>
- ok: convert numeric value to single-character string and vice-versa


!! MATCH$()
- <A HREF="..\test\test520.a">..\test\test520.a</A>
- ok: substring extraction (by pattern match)
- <A HREF="..\test\test520e.a">..\test\test520e.a</A>
- error: substring position


!! SEGBEG(), SEGEND(), SEGLEN() and SEGOFF()
- <A HREF="..\test\test522.a">..\test\test522.a</A>
- ok: correct segment data (16-bit)
- <A HREF="..\test\test522b.a">..\test\test522b.a</A>
- ok: correct segment data (24-bit)
- <A HREF="..\test\test522c.a">..\test\test522c.a</A>
- ok: correct segment data (32-bit)
- <A HREF="..\test\test522e.a">..\test\test522e.a</A>
- error: malformed (detectefirst pass)
- <A HREF="..\test\test522f.a">..\test\test522f.a</A>
- error: reference to unknown segments (segmented source)
- <A HREF="..\test\test522g.a">..\test\test522g.a</A>
- error: reference to unknown segments (monolithic source)
- <A HREF="..\test\test522h.a">..\test\test522h.a</A>
- error: uninitialized segments have no segment offset
- <A HREF="..\test\test522i.a">..\test\test522i.a</A>
- error: bad segment names
- <A HREF="..\test\test522j.a">..\test\test522j.a</A>
- error: malformed (detected second pass)


!! CPU$()
- <A HREF="..\test\test524.a">..\test\test524.a</A>
- ok: name of current CPU
- <A HREF="..\test\test524e.a">..\test\test524e.a</A>
- warning: CPU not set


!! TIME$()
- <A HREF="..\test\test526.a">..\test\test526.a</A>
- ok: time and date


!! MESG$()
- <A HREF="..\test\test528.a">..\test\test528.a</A>
- ok: internal message texts


!! FILE$()
- <A HREF="..\test\test530.a">..\test\test530.a</A>
- ok: current file name


!! LABEL()
- <A HREF="..\test\test532.a">..\test\test532.a</A>
- ok: symbol name existence testing


!! ISMACRO()
- <A HREF="..\test\test534.a">..\test\test534.a</A>
- ok: macro name existence testing


!! ABS()
- <A HREF="..\test\test536.a">..\test\test536.a</A>
- ok: absolute value


!! ROOTFILE$()
- <A HREF="..\test\test538.a">..\test\test538.a</A>
- ok: name of root file


!! SGN()
- <A HREF="..\test\test540.a">..\test\test540.a</A>
- ok: sign


!! SEED() and RND()
- <A HREF="..\test\test542.a">..\test\test542.a</A>
- ok: random integers


!! Function Evaluation
- <A HREF="..\test\test550.a">..\test\test550.a</A>
- ok: function evaluation
- <A HREF="..\test\test550e.a">..\test\test550e.a</A>
- error: non-existent
- <A HREF="..\test\test550f.a">..\test\test550f.a</A>
- error: labels with same name as functions


! Custom Byte Order


!! Assume Non-Default Order
- <A HREF="..\test\test560.a">..\test\test560.a</A>
- ok: non-default BIT16
- <A HREF="..\test\test560b.a">..\test\test560b.a</A>
- ok: non-default BIT32
- <A HREF="..\test\test560e.a">..\test\test560e.a</A>
- warn\error: bad useage


! Nonstandard Byte


!! 16-bit BYTE
- <A HREF="..\test\test570.a">..\test\test570.a</A>
- ok: 16-bit PC, 16-bit Byte
- <A HREF="..\test\test570b.a">..\test\test570b.a</A>
- ok: 24-bit PC, 16-bit Byte
- <A HREF="..\test\test570c.a">..\test\test570c.a</A>
- ok: 32-bit PC, 16-bit Byte
- <A HREF="..\test\test570e.a">..\test\test570e.a</A>
- error:non-existent data storage pseudo ops


!! 16-bit String Literals
- <A HREF="..\test\test572.a">..\test\test572.a</A>
- ok: 16-bit PC, 16-bit Byte, UTF-16


!! 16-bit Motorola Basic TRecord
- <A HREF="..\test\test574.a">..\test\test574.a</A>
- ok: 16-bit PC, 16-bit Byte
- <A HREF="..\test\test574b.a">..\test\test574b.a</A>
- ok: 24-bit PC, 16-bit Byte
- <A HREF="..\test\test574c.a">..\test\test574c.a</A>
- ok: 32-bit PC, 16-bit Byte


!! 16-bit Intel Basic Hex Record
- <A HREF="..\test\test575.a">..\test\test575.a</A>
- ok: 16-bit PC, 16-bit Byte
- <A HREF="..\test\test575b.a">..\test\test575b.a</A>
- ok: 20-bit PC, 16-bit Byte
- <A HREF="..\test\test575c.a">..\test\test575c.a</A>
- ok: 32-bit PC, 16-bit Byte


!! 16-bit FILL and PADTO
- <A HREF="..\test\test576.a">..\test\test576.a</A>
- ok: 16-bit PC, 16-bit Byte
- <A HREF="..\test\test576b.a">..\test\test576b.a</A>
- ok: 24-bit PC, 16-bit Byte
- <A HREF="..\test\test576c.a">..\test\test576c.a</A>
- ok: 32-bit PC, 16-bit Byte


!! 16-bit PADFROM
- <A HREF="..\test\test577.a">..\test\test577.a</A>
- ok: 16-bit PC, 16-bit Byte
- <A HREF="..\test\test577b.a">..\test\test577b.a</A>
- ok: 24-bit PC, 16-bit Byte
- <A HREF="..\test\test577c.a">..\test\test577c.a</A>
- ok: 32-bit PC, 16-bit Byte


!! 16-bit HEX and INCBIN
- <A HREF="..\test\test578.a">..\test\test578.a</A>
- ok: 16-bit PC, 16-bit Byte


!! 32-bit BYTE
- <A HREF="..\test\test580.a">..\test\test580.a</A>
- ok: 16-Bit PC, 32-Bit Byte
- <A HREF="..\test\test580b.a">..\test\test580b.a</A>
- ok: 20-Bit PC, 32-Bit Byte
- <A HREF="..\test\test580c.a">..\test\test580c.a</A>
- ok: 32-Bit PC, 32-Bit Byte
- <A HREF="..\test\test580e.a">..\test\test580e.a</A>
- error:non-existent data storage pseudo ops


!! 32-bit String Literals
- <A HREF="..\test\test582.a">..\test\test582.a</A>
- ok: 16-bit PC, 32-bit Byte


!! 32-bit Motorola Basic URecord
- <A HREF="..\test\test584.a">..\test\test584.a</A>
- ok: 16-bit PC, 32-bit Byte
- <A HREF="..\test\test584b.a">..\test\test584b.a</A>
- ok: 24-bit PC, 32-bit Byte
- <A HREF="..\test\test584c.a">..\test\test584c.a</A>
- ok: 32-bit PC, 32-bit Byte
- <A HREF="..\test\test584d.a">..\test\test584d.a</A>
- ok: 32-bit PC, 32-bit Byte, 32-Byte Data Record


!! 32-bit Intel Basic Hex Record
- <A HREF="..\test\test585.a">..\test\test585.a</A>
- ok: 16-bit PC, 32-bit Byte
- <A HREF="..\test\test585b.a">..\test\test585b.a</A>
- ok: 20-bit PC, 32-bit Byte
- <A HREF="..\test\test585c.a">..\test\test585c.a</A>
- ok: 32-bit PC, 32-bit Byte


!! 32-bit FILL and PADTO
- <A HREF="..\test\test586.a">..\test\test586.a</A>
- ok: 16-bit PC, 32-bit Byte
- <A HREF="..\test\test586b.a">..\test\test586b.a</A>
- ok: 24-bit PC, 32-bit Byte
- <A HREF="..\test\test586c.a">..\test\test586c.a</A>
- ok: 32-bit PC, 32-bit Byte


!! 32-bit PADFROM
- <A HREF="..\test\test587.a">..\test\test587.a</A>
- ok: 16-bit PC, 32-bit Byte
- <A HREF="..\test\test587b.a">..\test\test587b.a</A>
- ok: 24-bit PC, 32-bit Byte
- <A HREF="..\test\test587c.a">..\test\test587c.a</A>
- ok: 32-bit PC, 32-bit Byte


!! 32-bit HEX and INCBIN
- <A HREF="..\test\test588.a">..\test\test588.a</A>
- ok: 16-bit PC, 32-bit Byte


! Miscellaneous


!! Timers
- <A HREF="..\test\test600.a">..\test\test600.a</A>
- ok: "--TIMER" pseudo ops
- <A HREF="..\test\test600e.a">..\test\test600e.a</A>
- error: "--TIMER" pseudo ops


!! Numbers and BIT--
- <A HREF="..\test\test601.a">..\test\test601.a</A>
- ok: numbers and "BYTE", "WORD", "REVWORD", "LONG" and "REVLONG" pseudo-ops


!! HEX
- <A HREF="..\test\test602.a">..\test\test602.a</A>
- ok: HEX pseudo op
- <A HREF="..\test\test602e.a">..\test\test602e.a</A>
- error: HEX pseudo op


!! FLOAT
- <A HREF="..\test\test603.a">..\test\test603.a</A>
- ok: Microsoft and BBC BASICs format
- <A HREF="..\test\test603b.a">..\test\test603b.a</A>
- ok: IEEE double, single, half precision
- <A HREF="..\test\test603c.a">..\test\test603c.a</A>
- ok: BBC 5-byte floats
- <A HREF="..\test\test603e.a">..\test\test603e.a</A>
- error: not decimal and range limits


!! User Messages w/ String Expressions
- <A HREF="..\test\test604.a">..\test\test604.a</A>
- echo\ok: ECHO
- <A HREF="..\test\test604e.a">..\test\test604e.a</A>
- warn: WARN
- <A HREF="..\test\test604f.a">..\test\test604f.a</A>
- warn\error: ERROR
- <A HREF="..\test\test604g.a">..\test\test604g.a</A>
- fatal: FATAL
- <A HREF="..\test\test604h.a">..\test\test604h.a</A>
- fatal: FATAL
- <A HREF="..\test\test604i.a">..\test\test604i.a</A>
- warn\fatal: FATAL
- <A HREF="..\test\test604j.a">..\test\test604j.a</A>
- fatal: FATAL


!! Reserved Names
- <A HREF="..\test\test605.a">..\test\test605.a</A>
- ok: reserved name detection
- <A HREF="..\test\test605e.a">..\test\test605e.a</A>
- error: assignment to reserved names
- <A HREF="..\test\test605f.a">..\test\test605f.a</A>
- error: reserved names in expressions (detected second pass)
- <A HREF="..\test\test605g.a">..\test\test605g.a</A>
- error: user names which cannot match reserved names


!! User Stack
- <A HREF="..\test\test610.a">..\test\test610.a</A>
- echo\ok: "PUSHS" pseudo op and "POP$()" function
- <A HREF="..\test\test610b.a">..\test\test610b.a</A>
- echo\ok: "PUSHS" pseudo op and "POP$()" and "EMPTY()" functions
- <A HREF="..\test\test610c.a">..\test\test610c.a</A>
- echo\ok: "PUSHS" pseudo op and "PEEK$()" and "POP$()" functions
- <A HREF="..\test\test610e.a">..\test\test610e.a</A>
- error: bad arguments to "PUSHS" pseudo op
- <A HREF="..\test\test610f.a">..\test\test610f.a</A>
- fatal: stack overflow (default stack size)
- <A HREF="..\test\test610g.a">..\test\test610g.a</A>
- fatal: stack overflow ("MAXSTACK" stack size)
- <A HREF="..\test\test610h.a">..\test\test610h.a</A>
- error: stack not empty at end of pass one
- <A HREF="..\test\test610i.a">..\test\test610i.a</A>
- error: malformed "PEEK$()" function
- <A HREF="..\test\test610j.a">..\test\test610j.a</A>
- error: "PEEK$()" function and empty stack and out of range arguments
