function fillCSTable() {
    $.getJSON('http://10.1.33.175/GameServerFinder/JSON/cs.json',
     function (jsonObj) {
        tbodyElem = document.getElementById("csServers");
        tbodyElem.innerHTML = "";
            trElem = tbodyElem.insertRow(tbodyElem.rows.length);
            trElem.className = "csTopRow"; 
            tdElem = trElem.insertCell(trElem.cells.length);
            tdElem.innerHTML = "IP";
            tdElem = trElem.insertCell(trElem.cells.length);
            tdElem.innerHTML = "Name";
            tdElem = trElem.insertCell(trElem.cells.length);
            tdElem.innerHTML = "Map";
            tdElem = trElem.insertCell(trElem.cells.length);
            tdElem.innerHTML = "Players";
            tdElem = trElem.insertCell(trElem.cells.length);
            tdElem.innerHTML = "Latency";

        if (typeof jsonObj.length === "undefined" || jsonObj.length === 0) {
                trElem = tbodyElem.insertRow(tbodyElem.rows.length);               
                tdElem = trElem.insertCell(trElem.cells.length);
                tdElem.innerHTML = "No Server Running";
                tdElem.className = "csRows";
                tdElem.colSpan = "5";
        }
        else {
            for (var i = 0; i < jsonObj.length ; i++){
                trElem = tbodyElem.insertRow(tbodyElem.rows.length);               
                tdElem = trElem.insertCell(trElem.cells.length);
                tdElem.innerHTML = jsonObj[i]["serverIP"];
                tdElem = trElem.insertCell(trElem.cells.length);
                tdElem.innerHTML = jsonObj[i]["serverName"];
                tdElem = trElem.insertCell(trElem.cells.length);
                tdElem.innerHTML = jsonObj[i]["serverMapName"];
                tdElem = trElem.insertCell(trElem.cells.length);
                tdElem.innerHTML = jsonObj[i]["serverPlayer"] + "/" + jsonObj[i]["serverPlayerMax"];
                tdElem = trElem.insertCell(trElem.cells.length);
                tdElem.innerHTML = jsonObj[i]["serverLatency"] + " ms";
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
