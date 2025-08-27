document.addEventListener("DOMContentLoaded", () => {
  const counters = document.querySelectorAll(".counter");
  const cards = document.querySelectorAll(".stat-card");
  const speed = 80;

  counters.forEach((counter, index) => {
    setTimeout(() => {
      cards[index].classList.add("visible");
    }, index * 150);

    const updateCount = () => {
      const target = +counter.getAttribute("data-target");
      const count = +counter.innerText;
      const increment = Math.ceil(target / speed);

      if (count < target) {
        counter.innerText = count + increment;
        setTimeout(updateCount, 20);
      } else {
        counter.innerText = target;
      }
    };

    setTimeout(updateCount, index * 150);
  });
});