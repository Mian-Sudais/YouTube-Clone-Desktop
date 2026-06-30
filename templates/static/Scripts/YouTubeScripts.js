







const searchForm = document.querySelector("form");
  const searchInput = document.querySelector("input[type='search']");
  const videoColumns = document.querySelectorAll(".col-md-4");
  const noResults = document.getElementById("no-results");

  searchForm.addEventListener("submit", function(e) {
    e.preventDefault();
    const query = searchInput.value.toLowerCase().trim();
    let found = false;

    videoColumns.forEach(col => {
      const card = col.querySelector(".video-card");
      const title = (card.getAttribute("data-title") || "").toLowerCase();
      const match = query === "" ? true : title.includes(query);
      col.style.display = match ? "block" : "none";
      if (match) found = true;
    });

    noResults.style.display = found ? "none" : "block";
  });



  



















  function handleSearch(e) {
    e.preventDefault();
    const query = document.getElementById("searchInput").value.trim().toLowerCase();
    const videoColumns = document.querySelectorAll(".col-md-4");
    const noResults = document.getElementById("no-results");
    let found = false;

    videoColumns.forEach(col => {
      const card = col.querySelector(".video-card");
      const title = (card.getAttribute("data-title") || "").toLowerCase();
      const match = query === "" ? true : title.includes(query);
      col.style.display = match ? "block" : "none";
      if (match) found = true;
    });

    noResults.style.display = found ? "none" : "block";
  }