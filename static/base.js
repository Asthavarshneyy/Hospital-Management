const body = document.querySelector("body"),
      sidebar = body.querySelector(".sidebar"),
      logo = body.querySelector(".logo"),
      image = body.querySelector(".image")
      toggle = body.querySelector(".toggle"),
      searchBtn = body.querySelector(".search-box")

      toggle.addEventListener("click", () =>{
        sidebar.classList.toggle("close");
        logo.classList.toggle("close");
        image.classList.toggle("close");
      })