function init(data, keys) {
    const perPage = data.per_page

    const page = data.page

    const total = data.total

    const totalPage = data.total_page

    const tableData = data.data

    function initPagination() {
        let html = ``

        if (totalPage > 3) {
            html += `<span class="pagination-button">В начало</span>`
        }

        for (let index = 1; index < totalPage + 1; index++) {
            if (index === page) {
                html += `<span class="pagination-button active">${index}</span>`  
            } else {
                html += `<span class="pagination-button">${index}</span>`  
            }       
        }

        if (totalPage > 3) {
            html += `<span class="pagination-button">В конец</span>`
        }

        $('#paginationData').html(html)
    }

    function initTable() {
        let theadHtml = ``

        let tbodyHtml = ``

        for (const key in keys) {
            theadHtml += `<th>${keys[key]}</th>`
        }

        tableData.forEach(item => {
            let tbodyItem = `<tr>`

            for (const key in keys) {
                tbodyItem += `<td>${item[key]}</td>`
            }

            tbodyItem += `</tr>`

            tbodyHtml += tbodyItem
        })
        
        $('#thead').html(theadHtml)
        $('#tbody').html(tbodyHtml)
    }

    function initInfo() {
        let maxItemsForThisPage = page * perPage

        $('#paginationInfo').html(`Записи с ${((page - 1) * perPage) + 1} по ${maxItemsForThisPage > total ? total : maxItemsForThisPage} из ${total}`)
    }


    initPagination()
    initTable()
    initInfo()
}