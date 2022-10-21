let i = 1;

function duplicate() {
    let original = document.getElementById('duplicater' + i);
    let clone = original.cloneNode(true); // "deep" clone
    clone.id = "duplicater" + ++i;

    let inputs = clone.getElementsByTagName("input")
    inputs[0].setAttribute("name", i + "_from")
    inputs[1].setAttribute("name", i + "_to")
    inputs[2].setAttribute("name", i + "_word")
    inputs[3].setAttribute("name", i + "_features")

    let select = clone.getElementsByTagName('select')
    select[0].setAttribute("name", i + '_pos')

    original.parentNode.appendChild(clone);

}