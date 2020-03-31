import List from "list.js";
import $ from "jquery";

let listObj1 = new List("existing-list", {
    valueNames: ["mst-name", "mst-ris", "mst-url"]
});

let listObj2 = new List("oparl-list", {
    valueNames: ["mst-title", "mst-url"]
});

let listObj3 = new List("possible-list", {
    valueNames: ["mst-name", "mst-url"]
});

$("#search-field").on("keyup", function () {
    let searchString = $(this).val();
    listObj1.search(searchString);
    listObj2.search(searchString);
    listObj3.search(searchString);
});