function headerAnimation() {
	addWindowScrollEvent = true;
	const header = document.querySelector('header.header');
	const startPoint = header.dataset.scroll ? header.dataset.scroll : 1;
	let scrollDirection = 0;
	let timer;
	document.addEventListener("windowScroll", function (e) {
		const scrollTop = window.scrollY;
		clearTimeout(timer);
		if (scrollTop >= startPoint) {
			!header.classList.contains('_header-scroll') ? header.classList.add('_header-scroll') : null;
		} else {
			header.classList.contains('_header-scroll') ? header.classList.remove('_header-scroll') : null;
		}
		scrollDirection = scrollTop <= 0 ? 0 : scrollTop;
	});
}
setTimeout(() => {
	if (addWindowScrollEvent) {
		let windowScroll = new Event("windowScroll");
		window.addEventListener("scroll", function (e) {
			document.dispatchEvent(windowScroll);
		});
	}
}, 0);
headerAnimation();

