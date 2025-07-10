const popup_overlay = document.querySelector('.popup-overlay')
const popup = document.querySelector('.popup')

const title_input = document.querySelector('.title_input')
const story = document.querySelector('.text_area')

const input = document.querySelector('.title_input')
const text_area = document.querySelector('.text_area')

function open_popup() {
    
    popup_overlay.style.display = 'flex'
    popup.style.display = 'flex'
}

function close_popup() {
    popup.style.display = 'none';
    popup_overlay.style.display = 'none';
    // Clear form fields when popup closes
    const titleInput = document.getElementById('title');
    const contentInput = document.getElementById('content');
    if (titleInput) titleInput.value = '';
    if (contentInput) contentInput.value = '';
}




// Dropdown menu logic for month and date picker
document.addEventListener('DOMContentLoaded', () => {
    // Close popup after successful entry form submission (HTMX)
    const entryForm = document.getElementById('entry_form');
    if (entryForm) {
        entryForm.addEventListener('htmx:afterRequest', function(event) {
            close_popup();
        });
    }

    const dropdownBtn = document.getElementById('dropdownBtn');
    const dropdownMenu = document.getElementById('dropdownMenu');
    const dropdownLabel = document.getElementById('dropdownLabel');
    const monthPicker = document.getElementById('monthPicker');
    const datePicker = document.getElementById('datePicker');
    const reset_btn = document.getElementById('reset_btn');
    // Reset button logic: clear month and date pickers, reset label
    if (reset_btn) {
        reset_btn.addEventListener('click', function(e) {
            e.preventDefault();
            if (monthPicker) monthPicker.value = '';
            if (datePicker) datePicker.value = '';
            if (dropdownLabel) dropdownLabel.textContent = '📆 Filter Journals ▼';
            if (dropdownMenu) dropdownMenu.classList.remove('show');
        });
    }

    if (dropdownBtn && dropdownMenu) {
        dropdownBtn.addEventListener('click', (e) => {
            e.preventDefault(); // Prevent form/button default
            dropdownMenu.classList.toggle('show');
        });
        // Hide dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!dropdownBtn.contains(e.target) && !dropdownMenu.contains(e.target)) {
                dropdownMenu.classList.remove('show');
            }
        });
    }

    if (monthPicker) {
        monthPicker.addEventListener('change', function() {
            if (this.value) {
                const [year, month] = this.value.split('-');
                const monthName = new Date(year, month - 1).toLocaleString('default', { month: 'long' });
                if (dropdownLabel) dropdownLabel.textContent = `📆 ${monthName} ${year}`;
                if (dropdownMenu) dropdownMenu.classList.remove('show');
            } else {
                if (dropdownLabel) dropdownLabel.textContent = '📆 Filter Journals ▼';
            }
        });
    }
    if (datePicker) {
        datePicker.addEventListener('change', function() {
            if (this.value) {
                const dateObj = new Date(this.value);
                const formatted = dateObj.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
                if (dropdownLabel) dropdownLabel.textContent = `📆 ${formatted}`;
                if (dropdownMenu) dropdownMenu.classList.remove('show');
            } else {
                if (dropdownLabel) dropdownLabel.textContent = '📆 Filter Journals ▼';
            }
        });
    }
});


// function add_journal() {

//     const parent_div = document.querySelector('.journals')

//     // creating elements and adding classes to it
//     const about_journal = document.createElement('div')
//     about_journal.classList.add('about_journal')

//     const journal_title = document.createElement('div')
//     journal_title.classList.add('journal_title')

//     const head_title = document.createElement('h3')
//     head_title.classList.add('head_title')

//     const date = document.createElement('h5')
//     date.classList.add('date')

//     const journal_content = document.createElement('p')
//     journal_content.classList.add('journal_content')



//     // rendering elements
//     parent_div.insertBefore(about_journal, parent_div.firstChild)
//     about_journal.appendChild(journal_title)
//     journal_title.appendChild(head_title)
//     journal_title.appendChild(date)
//     about_journal.appendChild(journal_content)

//     // putting values inside elements
//     head_title.innerHTML = title_input.value
//     journal_content.innerHTML = story.value

//     close_popup()

// }

// async function load_journals() {
//     try {
//         const res = await fetch('/api/entries')
//         const data  = await res.json()

//           if (!Array.isArray(data)) {
//             alert(data.message || 'Failed to load entries');
//             return;
//             }
            
//     const parent_div = document.querySelector('.journals')
//     parent_div.innerHTML = ''

//     data.forEach(entry => {

//         const about_journal = document.createElement('div')
//         about_journal.classList.add('about_journal')

//         const journal_title = document.createElement('div')
//         journal_title.classList.add('journal_title')

//         const head_title = document.createElement('h3')
//         head_title.classList.add('head_title')

//         const date = document.createElement('h5')
//         date.classList.add('date')

//         const journal_content = document.createElement('p')
//         journal_content.classList.add('journal_content')

//         // putting values inside elements
//         head_title.innerHTML = entry.title
//         journal_content.innerHTML = entry.content
//         // date.innerHTML = new Date().toLocaleDateString();

//         // rendering elements
//         parent_div.insertBefore(about_journal, parent_div.firstChild)
//         about_journal.appendChild(journal_title)
//         journal_title.appendChild(head_title)
//         journal_title.appendChild(date)
//         about_journal.appendChild(journal_content)
        
//         })
//     } catch (err) {
//         console.log('Error while loading your journals: ', err)
//         alert('something went wrong while loading your journals')
//     }
    
// }

// window.addEventListener('DOMContentLoaded', () => {
//   load_journals();
// });

// showToast('journal added')