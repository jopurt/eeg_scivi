if(IN_VISUALIZATION && HAS_INPUT["Body Data"]){
    var body = CACHE["Body"];
    if(!body){
        var container = $("<div/>", {
            css: {
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                height: "100%",
                width: "100%",
                overflow: "hidden"
            }
        });
        body = document.createElement("img");
        $(body).css({
            maxWidth: "100%",
            maxHeight: "100%",
            display: "block"
        });
        container.append(body);
        ADD_VISUAL(container[0]);

        CACHE["Body"] = body
    }
    if(INPUT["Body Data"] == "gamma"){
        body.src = "storage/body_gamma.png";
    }
    else if ((INPUT["Body Data"] == "beta")) {
        body.src = "storage/body_beta.png";
    }
    else if ((INPUT["Body Data"] == "alpha")) {
        body.src = "storage/body_alpha.png";
    }
    else if ((INPUT["Body Data"] == "theta")) {
        body.src = "storage/body_theta.png";
    }
    else if ((INPUT["Body Data"] == "delta")) {
        body.src = "storage/body_delta.png";
    }
} else {
    CACHE["Body"] = null
}