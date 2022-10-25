let i = 1;

function duplicate() {
    let original = document.getElementById('duplicater_' + i);
    let clone = original.cloneNode(true); // "deep" clone
    updateBlockID(clone, ++i)
    original.parentNode.appendChild(clone);
}

function updateBlockID(block, id){
    block.id = "duplicater_" + id
    let inputs = block.getElementsByTagName("input");
    inputs[0].setAttribute("name", id + "_from");
    inputs[1].setAttribute("name", id + "_to");
    inputs[2].setAttribute("name", id + "_word");
    inputs[3].setAttribute("name", id + "_features");

    let select = block.getElementsByTagName('select');
    select[0].setAttribute("name", id + '_upos');

    let button = block.getElementsByTagName('a');
    button[button.length-1].setAttribute("id", 'close_' + id);
}


function removeBlock(clicked_id) {
    let id = Number(clicked_id.split('_')[1]);
    let all_blocks = document.querySelectorAll('[id^="duplicater"]');
    document.getElementById('duplicater_' + id).remove();
    --i
    for (let k = id; k < all_blocks.length; k++) {
        updateBlockID(all_blocks[k], Number(all_blocks[k].id.split('_')[1]) - 1)
    }
}