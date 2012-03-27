function fillCSTable() {
    var sourceURL = document.URL.split("/")
    if (sourceURL[sourceURL.length-1] === "index.html")
        delete sourceURL[sourceURL.length-1]
    var jsonURL = sourceURL.join("/") + "JSON/cs.json";
    $.getJSON(jsonURL, function (jsonObj) {
        tbodyElem = document.getElementById("csServers");
        tbodyElem.innerHTML = "";
        jsonDict = JSON.parse(jsonObj[0]);
        trElem = tbodyElem.insertRow(tbodyElem.rows.length);
        trElem.className = "csTopRow";
        tdElem = trElem.insertCell(trElem.cells.length);
        tdElem.innerHTML = jsonDict["serverName"];
        tdElem.className = "csServerName";
        tdElem = trElem.insertCell(trElem.cells.length);
        tdElem.innerHTML = jsonDict["serverMapName"];
        tdElem.className = "csServerMapName";
        tdElem = trElem.insertCell(trElem.cells.length);
        tdElem.innerHTML = jsonDict["serverIP"];
        tdElem.className = "csServerIP";
        tdElem = trElem.insertCell(trElem.cells.length);
        tdElem.innerHTML = jsonDict["serverLatency"];
        tdElem.className = "csServerLatency";
        tdElem = trElem.insertCell(trElem.cells.length);
        tdElem.innerHTML = jsonDict["serverPlayer"];
        tdElem.className = "csServerPlayer";
        tdElem = trElem.insertCell(trElem.cells.length);
        tdElem.innerHTML = "Player List";
        tdElem.className = "csServerPlayerList";

        if (jsonObj.length === 1) {
                trElem = tbodyElem.insertRow(tbodyElem.rows.length);
                trElem.className = "csRows noServerRow";
                tdElem = trElem.insertCell(trElem.cells.length);
                tdElem.innerHTML = "No Server Running";
                tdElem.colSpan = "6";
        }
        else {
            for (var i = 0; i < jsonObj.length ; i++){
                jsonDict = JSON.parse(jsonObj[i]);
                trElem = tbodyElem.insertRow(tbodyElem.rows.length);
                trElem.className = "csRow";
                tdElem = trElem.insertCell(trElem.cells.length);
                tdElem.innerHTML = jsonDict["serverName"];
                tdElem = trElem.insertCell(trElem.cells.length);
                tdElem.innerHTML = jsonDict["serverMapName"];
                tdElem = trElem.insertCell(trElem.cells.length);
                tdElem.innerHTML = jsonDict["serverIP"];
                tdElem = trElem.insertCell(trElem.cells.length);
                tdElem.innerHTML = jsonDict["serverLatency"] + " ms";
                tdElem = trElem.insertCell(trElem.cells.length);
                tdElem.innerHTML = jsonDict["serverPlayer"] + "/" + jsonDict["serverPlayerMax"];
            }
        }
     });
}

function refreshCSTable() {
    fillCSTable();
    setTimeout("refreshCSTable()", 10000);
}

jQuery(document).ready(function() {
    refreshCSTable();
});
