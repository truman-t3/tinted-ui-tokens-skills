# Tinted UI Design Principles

Distilled from the essay 《你的UI廉价，错在颜色》. These are the rules the
generator enforces. Read this when you need to explain *why* a token looks the
way it does, or when hand-tuning a system the script produced.

## The one decision

Cheap-looking UIs use **pure neutral colors**: `#FFFFFF`, `#000000`, `#808080`.
Expensive-looking UIs never do. Every neutral surface carries a few percent of
the brand hue. Brand color does not sit *on top* of the design — it *flows
through* it.

## Where the temperature lives (3 core places)

1. **Backgrounds & surfaces** — mix the brand color into the gray ramp. The
   background leans toward the brand; cards, borders and muted text lean too.
   The shift is tiny (2–3%) but it is what separates "designed" from "assembled".
2. **Shadows** — never `rgba(0,0,0,0.1)`. A shadow is light *absence*; it takes
   the temperature of the surrounding light. Blue brand → blue-violet shadow;
   warm brand → amber shadow. Keep alpha very low. The `0 0 0 1px` hairline
   border is part of the same shadow system and inherits its temperature.
3. **Text hierarchy** — primary text is near-black with a hue lean, not `#000`.
   Muted text follows the brand's warm/cool direction, not flat gray. Values
   still pass WCAG AA at body sizes — temperature is added inside the existing
   contrast budget, never at the cost of readability. **The generator now
   enforces this automatically**: every text-on-surface pair is measured with
   the WCAG 2.1 relative-luminance formula and, if it falls below AA
   (4.5:1 normal / 3:1 muted), the text is nudged along its HSL lightness axis
   until it passes — so readability always wins, and the brand hue-lean is kept
   wherever lightness does not hit an extreme.

## Three extensions (where systems usually break)

4. **Semantic colors** — error/warning/success must also be nudged toward the
   brand temperature (about 6–10° on the hue wheel). A red error in a blue
   product is "correct signal, wrong temperature" — like a fire alarm in a
   library. Keep it red, just lean it a few degrees. Their *subtle* backgrounds
   must lean toward the brand field, not default pink/amber/green.
5. **Gradients** — both stops must be tinted; never let one end drift to pure
   white. Direction should match natural light on a surface of that temperature
   (cool: deep-blue corner → light blue-white center; warm: deep amber bottom →
   cream top). Mesh gradients: every radial point carries brand hue, base is the
   tinted `--color-bg`, never `#FFFFFF`.
6. **Icons & illustration** — icon stroke color IS the text token (same stack,
   not an approximation). Icon container background IS `--color-brand-subtle`.
   Illustration shadows are derived from the same token family as UI shadows, so
   illustration and chrome look lit by one source.

## The test

Desaturate the whole interface to grayscale. If hierarchy still holds, the
temperature work is correct and invisible. If it collapses, the hue was doing
too much structural work — fix the gray ramp first, then re-add temperature.

## Three rules, no exceptions

- Never use pure neutral colors. Every neutral gets a hue, even 2%.
- Shadow color matches brand temperature. Pure black shadows belong to no system.
- Every interactive state (hover/focus/active) is tinted with `--color-brand-subtle`
  or a slightly more saturated surface — never a flat gray overlay.
