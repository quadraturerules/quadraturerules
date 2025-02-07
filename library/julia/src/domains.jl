@enum Domain begin
    {{for D in domains}}
    Domain_{{D.PascalCaseName}} = {{D.index}}
    {{end for}}
end

export Domain
