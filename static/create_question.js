
var inps = [];

function addInput() {
    var container = $(document).find("#option-container");
    var newInput = $("<input>", {type: "text", "class": "wide", "name": String(inps.length)});
    var li = $("<li></li>");
    $(li).append(newInput);
    $(container).append(li);
    inps.push(li);
}

function removeInput() {
    $(inps[inps.length-1]).remove();
    inps.pop();
}

function mySubmit() {
    console.log($("#title").val());
    if ($("#title").val().length < 1) {
        alert("Please enter a question title.");
        return;
    }
    if (inps.length < 2) {
        alert("You need at least 2 options for a valid question.");
        return;
    }
    for (let i = 0; i < inps.length; i ++) {
        if ($(inps[i]).children().first().val().length < 1) {
            alert("Please enter valid multiple choice options.");
            return;
        }
        for (let j = i+1; j < inps.length; j ++) {
            if ($(inps[i]).children().first().val() == $(inps[j]).children().first().val()) {
                alert("Multiple choice options should be unique.");
                return;
            }
        }
    }
    var form = $(document).find("#main-form");
    form.submit();
}
