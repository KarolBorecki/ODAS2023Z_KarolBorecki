function getFrequency(string) {
    var freq = {}
    for (var i = 0; i < string.length; i++) {
        var character = string.charAt(i)
        if (freq[character]) {
            freq[character]++
        } else {
            freq[character] = 1
        }
    }

    return freq
};

function entrophy(string) {
    const len = string.length
    const stat = getFrequency(string)
    let H = 0.0
    for (var i = 0; i < string.length; i++) {
        const p_i = stat[string.charAt(i)] / len
        H += p_i * Math.log2(p_i)
    }
    return -H
}


export function checkpassword(password) {
    const e = entrophy(password)
    return Math.max(0, Math.min(100, e * 17))
}