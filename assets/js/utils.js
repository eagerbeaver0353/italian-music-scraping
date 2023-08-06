let channels = ["spotify", "youtube", "shazam", "tiktok" /*, "radio"*/];

let weightIds = channels.map((item) => `#${item}-weight`);
let channelIds = channels.map((item) => `#${item}-checkbox`);
let channelWeights = channels.map((item) => 1);

function checkValidDate(id) {
    let periodType = $("#time-period-type").val();
    let regExp =
        periodType == "year"
            ? /\d{4}/g
            : periodType == "month"
            ? /\d{4}-\d{2}/g
            : /\d{4}-\d{2}-\d{2}/g;

    return $(id).prop("disabled") == true || regExp.test($(id).val()) == true;
}

function saveAsFile(content) {
    // Create element with <a> tag
    const link = document.createElement("a");

    // Create a blog object with the file content which you want to add to the file
    const file = new Blob([content], { type: "application/zip" });

    // Add file content in the object URL
    link.href = URL.createObjectURL(file);

    // Add file name
    link.download = "result.zip";

    // Add click event to <a> tag to save file.
    link.click();
    URL.revokeObjectURL(link.href);
}

function setDatePickerFormat(domSelector, type) {
    $(domSelector).datepicker("destroy");

    let datePickerParams = {
        defaultDate: new Date(),
        format:
            type == "year"
                ? "yyyy"
                : type == "month"
                ? "yyyy-mm"
                : "yyyy-mm-dd",
        viewMode:
            type == "year" ? "years" : type == "month" ? "months" : "days",
    };

    datePickerParams["minViewMode"] = datePickerParams["viewMode"];
    $(domSelector).datepicker(datePickerParams);
}

function handleTimePeriodType(value) {
    setDatePickerFormat("#start-date", value);
    setDatePickerFormat("#end-date", value);
    $("#end-date").attr("disabled", value != "custom");
}

$(function () {
    //Initialization
    setTimeout(() => {
        handleTimePeriodType("year");
    });

    //Attach Handlers
    $("#time-period-type").on("change", (e) =>
        handleTimePeriodType(e.target.value)
    );

    $("#channel-panel").on("change", (e) => {
        console.log(e.target.value);
        switch (e.target.value) {
            case "all":
                channelIds.forEach((id) => $(id).prop("checked", true));
                break;
            case "single":
                let filled = false;
                channelIds.forEach((id) => {
                    if (filled == true) $(id).prop("checked", false);
                    else if ($(id).prop("checked") == true) filled = true;
                });
                break;
            case "multiple":
                break;
        }
    });
    channelIds.forEach((id) => {
        $(id).on("change", (e) => {
            e.preventDefault();
            e.stopPropagation();
            console.log($("#channel-panel").val());
            switch ($("#channel-panel").val()) {
                case "all":
                    $(id).prop("checked", true);
                    break;
                case "single":
                    if (e.target.checked == true)
                        channelIds.forEach(
                            (_id) => id != _id && $(_id).prop("checked", false)
                        );
                    console.log(e.target.checked);
                    $(id).prop("checked", true);
                    break;
                case "multiple":
                    if (
                        e.target.checked == false &&
                        channelIds.filter(
                            (_id) => $(_id).prop("checked") == true
                        ).length == 0
                    )
                        $(id).prop("checked", true);
                    break;
            }
        });
    });

    $("#weights").on("change", (e) => {
        switch (e.target.value) {
            case "default":
                weightIds.forEach((id) => {
                    $(id).val(1);
                    $(id).prop("disabled", true);
                    channelWeights = channels.map((item) => 1);
                });
                break;
            case "custom":
                weightIds.forEach((id) => {
                    $(id).prop("disabled", false);
                });
                break;
        }
    });

    weightIds.forEach((id, index) => {
        $(id).on("change", (e) => {
            console.log(e.target.value);
            channelWeights[index] = parseInt(e.target.value);
            console.log(channelWeights);
        });
    });
    $("form").on("submit", function (e) {
        e.preventDefault();
        e.stopPropagation();

        let formData = {};
        channels.forEach(
            (item, index) =>
                (formData[item] = $(channelIds[index]).prop("checked")
                    ? channelWeights[index]
                    : 0)
        );
        console.log(formData);
        if (!checkValidDate("#start-date") || !checkValidDate("#end-date")) {
            alert("Please input valid date");
            return;
        }

        $("#spinner").css("visibility", "visible");
        $("div.___spanner").addClass("___show");
        $("div.___overlay").addClass("___show");

        fetch($(this).prop("action"), {
            method: "POST",
            mode: "cors",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                start_date: $("#start-date").val(),
                end_date:
                    $("#end-date").prop("disabled") == true
                        ? undefined
                        : $("#end-date").val(),
                data: formData,
            }),
        })
            .then((res) => res.blob())
            .then((blob) => saveAs(blob, "result.zip"))
            .catch((err) => alert(err))
            .finally(() => {
                $("#spinner").css("visibility", "hidden");
                $("div.___spanner").removeClass("___show");
                $("div.___overlay").removeClass("___show");
            });
    });
});
