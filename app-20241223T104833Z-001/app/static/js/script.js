window.onload = function () {
    let xhr = new XMLHttpRequest()
    let url = "https://dummyjson.com/comments?limit=10"

    xhr.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
           let response = JSON.parse(this.response)
           response.comments.forEach(comment => {
                let cardDiv = document.createElement("div")
                cardDiv.setAttribute("class", "card mt-3 mb-2")
                let cardBody = document.createElement("div")
                cardBody.setAttribute("class", "card-body")
                let blockquote = document.createElement("blockquote")
                blockquote.setAttribute("class", "blockquote mb-0")
                let text = document.createElement("p")
                text.innerHTML = comment.body
                let footer = document.createElement("footer")
                footer.setAttribute("class", "blockquote-footer")
                footer.innerHTML = comment.user.username

                blockquote.append(text, footer)
                cardBody.append(blockquote)
                cardDiv.append(cardBody)
                let sectionReview = document.getElementById("reviews")
                sectionReview.append(cardDiv)
           })
        }
    }
    xhr.open("GET", url, true)
    xhr.send()
}