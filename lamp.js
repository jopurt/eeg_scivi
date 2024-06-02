if(IN_VISUALIZATION && HAS_INPUT["Lamp Data"]){
    var light = CACHE["Light"];
    if(!light){
        var container = $("<div/>", {
            css: {
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                height: "100%",
                width: "100%"
            }
        });
        light = document.createElement("img");
        container.append(light);
        ADD_VISUAL(container[0]);

        CACHE["Light"] = light
    }

    if(INPUT["Lamp Data"] == true){
        light.src = "storage/lamp_on.png";
    } else if ((INPUT["Lamp Data"] == false)) {
        light.src = "storage/lamp_off.png";
    }
} else {
    CACHE["Light"] = null
}