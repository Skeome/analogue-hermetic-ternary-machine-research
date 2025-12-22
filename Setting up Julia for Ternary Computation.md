# Install Julia using curl
```
curl -fsSL https://install.julialang.org | sh
```
Once Julia is installed, type `julia` and hit return to enter the Julia REPL environment
If you've copied `ternary.jl` you can automatically set up the environment by typing `include("ternary.jl")`
# Declare Ternary Operations

## Trit
```
@enum Trit begin
Neg = -1
Zero = 0
Pos = 1
end
```

## tNOT Gate
```
function tNOT(t::Trit)
return Trit(-Int(t))
end
```

## tAND Gate
```
function tAND(a::Trit, b::Trit)
return Trit(min(Int (a), Int(b)))
end
```

## tOR Gate
```
function tOR(a::Trit, b::Trit)
return Trit(max(Int(a), Int(b)))
end
```

## tNAND Gate
```
function tNAND(a::Trit, b::Trit)
return tNOT(tAND(a, b))
end
```

## tNOR Gate
```
function tNOR(a::Trit, b::Trit)
return tNOT(tOR(a, b))
end
```

## tShiftUp
```
function tShiftUp(t::Trit)
if t == Pos
return Neg
else return Trit(Int(t) + 1)
end
end
```

## tShiftDown
```
function tShiftDown(t::Trit)
if t == Neg
return Pos
else return Trit(Int(t) - 1)
end
end
```

## tSUM
```
function tSUM(a::Trit, b::Trit)
s = Int(a) + Int(b)
if s > 1
return Neg   # 1 + 1 = 2, which is (1, -1) in ternary. Sum is -1.
elseif s < -1
return Pos   # -1 + -1 = -2, which is (-1, 1) in ternary. Sum is 1.
else
return Trit(s)
end
end
```

## tCONSENSUS
```
function tCONSENSUS(a::Trit, b::Trit)
s = Int(a) + Int(b)
if s > 1
return Pos   # Carry the 1
elseif s < -1
return Neg   # Carry the -1
else
return Zero  # No overflow
end
end
```

## Override + Logic for Trits
```
import Base: +

function (Base.:+)(a::Trit, b::Trit)
return tSUM(a, b)
end
```

```
# This simulates an analogue signal being "cleaned up" into a Trit
function analogueToTrit(voltage::Float64)
# Any voltage > 0.5 becomes 1, < -0.5 becomes -1, else 0
if voltage > 0.5
return Pos
elseif voltage < -0.5
return Neg
else
return Zero
end
end
```
```
mutable struct TritRegister
    value::Trit
end

# Let's create a register starting at Zero
my_register = TritRegister(Zero)
```
```
function clock_tick!(reg::TritRegister)
    reg.value = tROTATE_UP(reg.value)
    println("Register state: ", reg.value)
end
```

```
function noisy_input()
    # Returns a random number near 1.0, 0.0, or -1.0
    states = [-1.0, 0.0, 1.0]
    return rand(states) + (rand() - 0.5) * 0.1 
end
```

```
function decode_analogue(voltage::Float64)
    if voltage > 0.5
        return Pos
    elseif voltage < -0.5
        return Neg
    else
        return Zero
    end
end
```

```
# 1. Initialize the machine state
accumulator = TritRegister(Zero)

# 2. Simulate a stream of "Analogue" voltages
# These represent noisy signals from a sensor or another circuit
test_voltages = [0.98, 1.1, -0.85, 0.1, -1.2]

println("Starting Simulation...")
println("Initial Register: ", accumulator.value)
println("---")

for (i, v) in enumerate(test_voltages)
    # Step A: Convert analogue to discrete trit
    incoming_trit = decode_analogue(v)
    
    # Step B: Perform Ternary Addition (Hermetic logic)
    # We use the '+' we overloaded earlier!
    new_value = accumulator.value + incoming_trit
    
    # Step C: Update the register
    accumulator.value = new_value
    
    println("Cycle $i: Voltage $v -> Trit $incoming_trit")
    println("New Accumulator State: $(accumulator.value)")
    println("---")
end
```

## tMUX
```
function tMUX(s::Trit, a::Trit, b::Trit, c::Trit)
    if s == Neg
        return a
    elseif s == Zero
        return b
    else
        return c
    end
end
```

## 1 Tryte Memory Bank
```
# Create an array of 9 Trits, all initialized to Zero
memory_bank = fill(Zero, 9)

# Change the 5th trit to Pos
memory_bank[5] = Pos

# See the whole bank
println(memory_bank)
```

## Simulate voltage drops
```
# Simulate a signal losing strength over a long wire
function simulate_wire(input_v::Float64, resistance::Float64)
    # The signal gets weaker (multiplied by 0.8) and picks up noise
    return (input_v * resistance) + (rand() - 0.5) * 0.05
end

# Test it:
strong_signal = 1.0  # A clean 'Pos'
weak_signal = simulate_wire(strong_signal, 0.6) # 40% loss
println("Signal after wire: ", weak_signal)

# Use our decoder to see if the machine can still read it correctly
println("Decoded Trit: ", decode_analogue(weak_signal))
```

## tEQ
```
function tEQ(a::Trit, b::Trit)
    return a == b ? Pos : Neg
end
```

## Add "Plots" Package
```
using Pkg
Pkg.add("Plots")
using Plots
```

## Simulate and Plot Signal over Time
```
# 1. Start a fresh plot with the analogue data
p = plot(time_steps, raw_voltages, 
    label="Analogue Voltage", 
    color=:blue, 
    lw=1.5)

# 2. Add the decoded trits using 'steppost' to show discrete jumps
plot!(p, time_steps, decoded_trits, 
    label="Decoded Trit", 
    color=:red, 
    seriestype=:steppost, 
    lw=2)

# 3. Add labels and show
xlabel!("Time")
ylabel!("Signal Level")
hline!([-0.5, 0.5], color=:black, linestyle=:dash, label="Thresholds") # Added thresholds!
```


```
function balanced_ternary_to_int(trits::Vector{Trit})
    total = 0
    # We iterate through the trits. 
    # Usually, the first element [1] is the least significant (3^0)
    for (i, t) in enumerate(trits)
        exponent = i - 1
        total += Int(t) * (3^exponent)
    end
    return total
end
```

## Test
```
# Represents (1 * 3^0) + (1 * 3^1) + (-1 * 3^2) = 1 + 3 - 9 = -5
my_tryte = [Pos, Pos, Neg] 
balanced_ternary_to_int(my_tryte)
```



```
# Inputs: 0.55V (Barely a 'Pos') and 0.6V (Barely a 'Pos')
# Mathematically: 1 + 1 = 2. 
# In Ternary: Sum = -1 (Neg), Carry = 1 (Pos)

voltage_a = 0.55
voltage_b = 0.60

# Step 1: Hardware-level decoding
trit_a = decode_analogue(voltage_a)
trit_b = decode_analogue(voltage_b)

# Step 2: Logic-level addition
s, c = tFULL_ADDER(trit_a, trit_b, Zero)

println("Analogue Inputs: $voltage_a V, $voltage_b V")
println("Decoded Trits:   $trit_a, $trit_b")
println("-------------------------")
println("Machine Sum:     $s")
println("Machine Carry:   $c")
```

## Find Failure Point
```
# We know 1.0V + 1.0V should always result in a Carry of 'Pos'
# Let's see how much "Voltage Drop" we can survive.

println("Voltage | Decoded | Carry Result | Status")
println("-----------------------------------------")

for v in 1.0:-0.1:0.0
    t = decode_analogue(v)
    # We add two identical trits
    s, c = tFULL_ADDER(t, t, Zero)
    
    status = (c == Pos) ? "PASS" : "FAIL"
    
    println("$(rpad(v, 7)) | $(rpad(t, 7)) | $(rpad(c, 12)) | $status")
end
```
### Result
```
julia> # We know 1.0V + 1.0V should always result in a Carry of 'Pos'
       # Let's see how much "Voltage Drop" we can survive.

       println("Voltage | Decoded | Carry Result | Status")
Voltage | Decoded | Carry Result | Status

julia> println("-----------------------------------------")
-----------------------------------------

julia> for v in 1.0:-0.1:0.0
           t = decode_analogue(v)
           # We add two identical trits
           s, c = tFULL_ADDER(t, t, Zero)
           
           status = (c == Pos) ? "PASS" : "FAIL"
           
           println("$(rpad(v, 7)) | $(rpad(t, 7)) | $(rpad(c, 12)) | $status")
       end
1.0     | Pos     | Pos          | PASS
0.9     | Pos     | Pos          | PASS
0.8     | Pos     | Pos          | PASS
0.7     | Pos     | Pos          | PASS
0.6     | Pos     | Pos          | PASS
0.5     | Zero    | Zero         | FAIL
0.4     | Zero    | Zero         | FAIL
0.3     | Zero    | Zero         | FAIL
0.2     | Zero    | Zero         | FAIL
0.1     | Zero    | Zero         | FAIL
0.0     | Zero    | Zero         | FAIL
```
