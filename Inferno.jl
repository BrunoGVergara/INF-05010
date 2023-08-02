using Pkg, JuMP, Cbc, CSV, DataFrames 

DF = CSV.read("file1.csv", DataFrame, header = false)

NP = parse(Float64, DF[1, 1])
NS = parse(Float64, DF[1, 2])

println(typeof(NP))

S = Vector{Float64}()

for i in 3 : 3 + NP
    number = DF[i, 4]
    push!(S, number)
end

println(S)