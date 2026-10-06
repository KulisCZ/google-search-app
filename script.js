const button = document.querySelector("button");
const input = document.querySelector("#query");
const result = document.querySelector("#result");
const saveButton = document.querySelector("#save");
let searchResults = [];

button.addEventListener("click", function() {
	if (input.value === "") {
    result.textContent = "Enter a term in searchbox first";
    return;
}
	result.innerHTML = "";
    fetch("/search?query=" + input.value)
        .then(function(response) {
			if (!response.ok) {
			throw new Error("Error during search");
    }

    return response.json();
})
        .then(function(data) {
			searchResults = data;
			
            for (let i = 0; i < data.length; i++) {
				
                result.innerHTML +=
                    "<a href='" + data[i].link + "'>" +
                    data[i].title +
                    "</a><br>" +
                    data[i].snippet +
                    "<br>";
            }
        })
		.catch(function(error) {
		console.log(error);
		result.textContent = "Something went wrong";
	});
});

saveButton.addEventListener("click", function() {
	if (searchResults.length === 0) {
    result.textContent = "Enter a term in searchbox first";
    return;
}
	
	const json = JSON.stringify(searchResults, null, 2);
		
	const blob = new Blob([json], { type: "application/json" });
	
	const url = URL.createObjectURL(blob);
	
	const link = document.createElement("a");
	link.href = url;
	link.download = "search-results.json";
	link.click();
});