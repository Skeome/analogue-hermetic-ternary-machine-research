# ==========================================
# ANALOGUE-HERMETIC TERNARY RESEARCH CORE
# ==========================================

# 1. THE TRIT ENUM 
@enum Trit Neg=-1 Zero=0 Pos=1

# 2. MNEMONIC LOGIC GATES 
function tNOT(t::Trit)
    return Trit(-Int(t))
end

function tAND(a::Trit, b::Trit)
    return Trit(min(Int(a), Int(b)))
end

function tOR(a::Trit, b::Trit)
    return Trit(max(Int(a), Int(b)))
end

function tNAND(a::Trit, b::Trit)
    return tNOT(tAND(a, b))
end

function tNOR(a::Trit, b::Trit)
    return tNOT(tOR(a, b))
end

function tEQ(a::Trit, b::Trit)
    return a == b ? Pos : Neg
end

function tMUX(s::Trit, a::Trit, b::Trit, c::Trit)
    if s == Neg; return a
    elseif s == Zero; return b
    else return c; end
end

# Rotates values: -1 -> 0, 0 -> 1, 1 -> -1 
function tROTATE_UP(t::Trit)
    return t == Pos ? Neg : Trit(Int(t) + 1)
end

function tROTATE_DOWN(t::Trit)
    return t == Neg ? Pos : Trit(Int(t) - 1)
end

# 3. OPERATOR OVERLOADING 
import Base: +, &, |
(Base.:+)(a::Trit, b::Trit) = tSUM(a, b)
(Base.:&)(a::Trit, b::Trit) = tAND(a, b)
(Base.:|)(a::Trit, b::Trit) = tOR(a, b)

# 4. ARITHMETIC (Hermetic Full Adder & Multi-Trit)
function tSUM(a::Trit, b::Trit)
    s = Int(a) + Int(b)
    if s == 2 return Neg
    elseif s == -2 return Pos
    else return Trit(s) end
end

function tCONSENSUS(a::Trit, b::Trit)
    s = Int(a) + Int(b)
    if s > 1 return Pos
    elseif s < -1 return Neg
    else return Zero end
end

# Robust Full Adder using Total Integer Sum
function tFULL_ADDER(a::Trit, b::Trit, cin::Trit)
    total = Int(a) + Int(b) + Int(cin)
    
    # Calculate Sum (Remainder base 3, balanced)
    if total == 3 || total == 0 || total == -3
        s_out = Zero
    elseif total == 1 || total == -2
        s_out = Pos
    else # total == -1 || total == 2
        s_out = Neg
    end
    
    # Calculate Carry (The 3s place)
    if total > 1
        c_out = Pos
    elseif total < -1
        c_out = Neg
    else
        c_out = Zero
    end
    
    return s_out, c_out
end

function add_trytes(word_a::Vector{Trit}, word_b::Vector{Trit})
    len = max(length(word_a), length(word_b))
    a = vcat(word_a, fill(Zero, len - length(word_a)))
    b = vcat(word_b, fill(Zero, len - length(word_b)))
    
    result = Trit[]
    carry = Zero
    for i in 1:len
        s, carry = tFULL_ADDER(a[i], b[i], carry)
        push!(result, s)
    end
    if carry != Zero; push!(result, carry); end
    return result
end

# Subtraction by negation (A + (-B))
function sub_trytes(word_a::Vector{Trit}, word_b::Vector{Trit})
    negative_b = [tNOT(t) for t in word_b]
    return add_trytes(word_a, negative_b)
end

# 5. ANALOGUE INTERFACE 
function decode_analogue(voltage::Float64)
    if voltage > 0.5; return Pos
    elseif voltage < -0.5; return Neg
    else return Zero; end
end

# 6. MEMORY & DATA FORMATTING 
mutable struct TritRegister
    value::Trit
end

function balanced_ternary_to_int(trits::Vector{Trit})
    total = 0
    for (i, t) in enumerate(trits)
        total += Int(t) * (3^(i-1))
    end
    return total
end

function tPRINT(trits::Vector{Trit})
    symbols = Dict(Pos => "+", Zero => "0", Neg => "-")
    println(join([symbols[t] for t in reverse(trits)]))
end

println(">>> Analogue-Hermetic Environment Loaded.")