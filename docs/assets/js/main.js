(function () {
  var targets = document.querySelectorAll(".squad-card, .agent-card, .tool-card, .step, .journey");
  if (!("IntersectionObserver" in window) || targets.length === 0) {
    targets.forEach(function (el) { el.classList.add("in-view"); });
    return;
  }
  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15, rootMargin: "0px 0px -40px 0px" }
  );
  targets.forEach(function (el) { observer.observe(el); });

  // stagger delays within each grid for a nicer cascade
  ["agents", "tools"].forEach(function (cls) {
    document.querySelectorAll("." + cls).forEach(function (grid) {
      Array.prototype.forEach.call(grid.children, function (card, i) {
        card.style.transitionDelay = Math.min(i * 60, 360) + "ms";
      });
    });
  });
  document.querySelectorAll(".grid").forEach(function (grid) {
    Array.prototype.forEach.call(grid.children, function (card, i) {
      card.style.transitionDelay = Math.min(i * 50, 400) + "ms";
    });
  });
  document.querySelectorAll(".journey").forEach(function (journey) {
    Array.prototype.forEach.call(journey.querySelectorAll(".step"), function (step, i) {
      step.style.transitionDelay = i * 90 + "ms";
    });
  });
})();
