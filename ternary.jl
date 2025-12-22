# ==========================================
# ANALOGUE-HERMETIC TERNARY RESEARCH CORE
# ==========================================

# 1. THE TRIT ENUM
@enum Trit Neg=-1 Zero=0 Pos=1

# 2. MNEMONIC LOGIC GATES (Standardized)
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
    if s > 1; return Neg   # 1 + 1 = 2 -> (1, -1)
    elseif s < -1; return Pos # -1 + -1 = -2 -> (-1, 1)
    else return Trit(s); end
end

function tCONSENSUS(a::Trit, b::Trit)
    s = Int(a) + Int(b)
    if s > 1; return Pos
    elseif s < -1; return Neg
    else return Zero; end
end

function tFULL_ADDER(a::Trit, b::Trit, cin::Trit)
    s1 = tSUM(a, b)
    c1 = tCONSENSUS(a, b)
    sum_final = tSUM(s1, cin)
    c2 = tCONSENSUS(s1, cin)
    cout = tOR(c1, c2) # Standard Hermetic carry logic
    return sum_final, cout
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

# 5. ANALOGUE INTERFACE
function decode_analogue(voltage::Float64)
    if voltage > 0.5; return Pos
    elseif voltage < -0.5; return Neg
    else return Zero; end
end

# 6. MEMORY, UTILS & FORMATTING
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

# Pretty printer: displays as +, 0, - (MSB on the left)
function tPRINT(trits::Vector{Trit})
    symbols = Dict(Pos => "+", Zero => "0", Neg => "-")
    println(join([symbols[t] for t in reverse(trits)]))
end

println(">>> Analogue-Hermetic Environment Loaded.")