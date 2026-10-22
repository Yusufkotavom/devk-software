/**
 * Progressive-enhancement for the scroll-snap sliders used by the Slider and
 * Feed blocks. Anything with [data-slider] that contains [data-track] gets
 * arrow + dot navigation wired to native horizontal scrolling. Bundled once
 * per page (Astro dedupes the module), so it is safe to import from several
 * components.
 */
function initSlider(root: HTMLElement) {
	const track = root.querySelector<HTMLElement>("[data-track]");
	if (!track) return;
	const prev = root.querySelector<HTMLButtonElement>("[data-prev]");
	const next = root.querySelector<HTMLButtonElement>("[data-next]");
	const dots = Array.from(root.querySelectorAll<HTMLButtonElement>("[data-dots] .slider__dot"));
	const slides = Array.from(track.children) as HTMLElement[];

	const step = () => {
		const first = slides[0];
		if (!first) return 300;
		const gap = parseFloat(getComputedStyle(track).columnGap || "16") || 16;
		return first.getBoundingClientRect().width + gap;
	};

	const update = () => {
		const currentStep = step();
		const i = Math.round(track.scrollLeft / currentStep) % (dots.length || 1);
		dots.forEach((dot, di) => dot.setAttribute("aria-current", di === i ? "true" : "false"));
		// Keep buttons always enabled for infinite loop
		if (prev) prev.disabled = false;
		if (next) next.disabled = false;
	};

	prev?.addEventListener("click", () => {
		const currentStep = step();
		if (track.scrollLeft <= 5) {
			track.scrollTo({ left: track.scrollWidth - track.clientWidth, behavior: "smooth" });
		} else {
			track.scrollBy({ left: -currentStep, behavior: "smooth" });
		}
	});

	next?.addEventListener("click", () => {
		const currentStep = step();
		if (track.scrollLeft >= track.scrollWidth - track.clientWidth - 5) {
			track.scrollTo({ left: 0, behavior: "smooth" });
		} else {
			track.scrollBy({ left: currentStep, behavior: "smooth" });
		}
	});

	dots.forEach((dot, di) =>
		dot.addEventListener("click", () => track.scrollTo({ left: di * step(), behavior: "smooth" })),
	);
	track.addEventListener("scroll", () => requestAnimationFrame(update), { passive: true });
	window.addEventListener("resize", update);
	update();
}

for (const root of document.querySelectorAll<HTMLElement>("[data-slider]")) initSlider(root);
