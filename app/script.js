
var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");

var color = "#000000"; // Default color

async function countWords() {
    var inputSentence = document.getElementById("textInput").value;

    // Remove leading and trailing whitespaces
    var trimmedSentence = inputSentence.trim();

    // Split the sentence into words using space as a delimiter
    var words = trimmedSentence.split(/\s+/);

    // Filter out empty words (occurs if there are multiple consecutive spaces)
    words = words.filter(function (word) {
        return word.length > 0;
    });

    //Word Freq Dict
    word_freq = {}

    //For Each word add count
    for (let i = 0; i < words.length;i++) {
        let word = words[i]
        //If word in Dictionary, add 1 to word
        if (word_freq[word]) {
            word_freq[word] += 1
        }
        //Else Add word to Dict & set 1
        else {
            word_freq[word] = 1
        }
    }

    // Display the word count
    var wordCount = words.length;
    document.getElementById("wordCountResult").innerText = "Word count: " + wordCount;
    //Return Word Freq
    return(word_freq)

}
async function addText() {
    //Get Word Freq
    var word_freq = await countWords()

    // Display words on the canvas
    var x = 10;
    var y = 30;
    var lineHeight = 30;
    var fontColor = document.getElementById("colorPicker").value || "blue";
    ctx.fillStyle = fontColor;
    console.log(word_freq)
    for (var key in word_freq) {
        var value = word_freq[key]
        ctx.font = value * 10 + "px Arial";
        
        // Check if the next line exceeds the canvas height
        if (y + lineHeight > canvas.height) {
            y = 30; // Reset y to a new starting position
            x += 150; // Move to a new column
        }

        ctx.fillText(key, x, y);
        y += lineHeight;
    }
}

function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

document.getElementById("colorPicker").addEventListener("input", function (e) {
    color = e.target.value;
});
