// ==UserScript==
// @name         Change images' resolution
// @version      1.0
// @description  [SingleFile] Replace img url with a higher resolution version
// ==/UserScript==


(() => {
    // Get the image element that has a src attribute and an empty alt(use to ignore profile images)
    const imgElementsSelector = "img[src][alt='']:not([src=''])";

    // Regex grouping[0] is the original string
    // Group[1] is the entire string before =s where everything after the domain name is between 30-85 characters
    // Group[2] will be used and set to 0 to obtain the max resolution of the image
    const pattern = "(https:\/\/yt3\.ggpht\.com\/.{30,85}=[a-z]{1})(.*)";

    dispatchEvent(new CustomEvent("single-file-user-script-init"));
    addEventListener("single-file-on-before-capture-request", () => {
        try {
            collapse_button = document.querySelector("ytd-sponsorships-expandable-perks-renderer");
            collapse_button.removeAttribute("is-collapsed");
        }
        catch (error) {
            console.log("Encountered Error");
            console.error(error);
        }
        // Only want images in the content element
        let content = document.getElementById("contents").getElementsByClassName("style-scope ytd-section-list-renderer")[0]
        content.querySelectorAll(imgElementsSelector).forEach(element => {
            try {
                let img_src = element.getAttribute("src");
                group_match = img_src.match(pattern);
                new_img_src = group_match[1] + '0';
                element.setAttribute("src", new_img_src);
            }
            catch (error) {
				console.log("Encountered Error");
                console.error(error);
            }
        });
		console.log("Finished script");
		return;
    });
})();


// (() => {
// dispatchEvent(new CustomEvent("single-file-user-script-init"));
//
// addEventListener("single-file-on-before-capture-request", () => {
//     link_holder = document.getElementById("links-holder");
//     link_holder.remove();
//     // Get the image element that has a src attribute and an empty alt(use to ignore profile images)
//     const imgElementsSelector = "img[src][alt='']:not([src=''])";
//
//     // Regex grouping[0] is the original string
//     // Group[1] is the entire string before =s where everything after the domain name is between 30-85 characters
//     // Group[2] will be used and set to 0 to obtain the max resolution of the image
//     const pattern = "(https:\/\/yt3\.ggpht\.com\/.{30,85}=[a-z]{1})(.*)";
//     Array.from(content.images).forEach(image => {
//         try{
//             group_match = image.src.match(pattern);
//             new_img_src = group_match[1] + '0';
//             image.src = new_img_src;
//         }catch(error) {
//             console.log(error);
//         }
// })});})();