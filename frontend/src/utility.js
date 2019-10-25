const showLengthLimit = 200;

export default {
    getBrief: (content) => {
        let brief = content.substring(0, Math.min(content.length, showLengthLimit))
        if (content.length > 200)
            brief += '...'
        return brief
    }
}