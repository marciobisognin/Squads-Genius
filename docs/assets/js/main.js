(function () {
  var boot = document.getElementById("boot-intro");
  var reducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (boot) {
    if (reducedMotion || sessionStorage.getItem("sg-boot-seen")) {
      boot.remove();
    } else {
      sessionStorage.setItem("sg-boot-seen", "1");
      runBootIntro(boot);
    }
  }

  function runBootIntro(el) {
    var DURATION = 4000;
    var lines = [
      "&gt; inicializando squads genius<b>_</b>",
      "&gt; carregando agentes e workflows<b>_</b>",
      "&gt; sincronizando ferramentas e scripts<b>_</b>",
      "&gt; compilando galeria de squads<b>_</b>",
      "&gt; pronto<b>_</b>"
    ];
    var terminal = el.querySelector("#boot-terminal");
    var fill = el.querySelector("#boot-fill");
    var pct = el.querySelector("#boot-pct");
    var content = el.querySelector(".boot-content");
    var breach = el.querySelector("#boot-breach");
    var bars = el.querySelector("#boot-breach-bars");
    document.body.style.overflow = "hidden";

    if (breach && bars) {
      for (var i = 0; i < 8; i++) {
        var span = document.createElement("span");
        span.style.top = (i * 13) + "%";
        bars.appendChild(span);
      }
    }

    lines.forEach(function (line, i) {
      var div = document.createElement("div");
      div.style.animationDelay = (i * (DURATION * 0.7 / lines.length)) + "ms";
      div.innerHTML = line;
      terminal.appendChild(div);
    });

    var start = null;
    function step(ts) {
      if (!start) start = ts;
      var elapsed = ts - start;
      var progress = Math.min(elapsed / DURATION, 1);
      var value = Math.round(progress * 100);
      fill.style.width = value + "%";
      pct.textContent = value + "%";
      if (progress < 1) {
        requestAnimationFrame(step);
      } else if (breach) {
        content.classList.add("fading");
        setTimeout(function () { breach.classList.add("active"); }, 200);
        setTimeout(function () { finishBoot(el); }, 3500);
      } else {
        finishBoot(el);
      }
    }
    requestAnimationFrame(step);
  }

  function finishBoot(el) {
    el.classList.add("boot-intro--done");
    document.body.style.overflow = "";
    setTimeout(function () { el.remove(); }, 500);
  }

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
