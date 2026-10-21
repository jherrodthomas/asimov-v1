# Change record: bench equipment for powered testing

| Field | Value |
|---|---|
| Change | Purchase of the bench equipment that the hold point [WP-V-07 §2](../../06-validation/WP-V-07-test-operations.md#2-conditions-before-any-powered-test-with-the-robot-assembled) requires: a rated portable gantry crane (500 kg class) with a trolley, a rated winch or self-retracting fall-arrest block, a tether and shackles rated for a 35 kg dynamic load; a dual-channel E-stop pendant with a certified safety relay module (Category 3 or better, monitored reset) and two contactors with mirror contacts; a laboratory power supply at the kit's rail voltage with an adjustable current limit and an output switch |
| Decided | 2026-10-21 by the project lead: DQ-035 A (one purchase), DQ-027 A (gantry crane), DQ-036 A (safety relay), DQ-037 A (bench supply), DQ-008 A (pendant), DQ-009 A (no battery) |
| Class | SR-A once fitted (the stop chain and the power path of CFG-001); bench equipment, not product design |
| Status | **Open: quotes to be entered below before ordering** (DQ-035 A) |
| Baseline | `a1380ac` |

## Hazards and safety functions touched

H-01, H-06, H-23, H-28 (the fall: carried by the gantry and tether, DM-01); H-11, H-28, H-29 and every limb hazard
(the wired pendant and contactors, DM-02, SF-13); H-08, H-09, H-13 (the bench supply in place of a battery, DM-03).
No existing safety function changes: none exists yet; the equipment is the complementary measure the first safety
case rests on (claims G2.2, G2.4).

## Work products re-opened

WP-V-07 (conditions C-1 to C-3 become met once the equipment exists and is tested), WP-C-02 §6 (the test area
around the gantry), WP-C-03 §6 (DM-01 to DM-03 status), WP-S-03 and WP-H-02 (the bench chain is the first instance
of the stop chain), WP-H-07 (the certificates of the safety relay and the gantry as component evidence), WP-M-03 §4
(budget).

## Quotes

| Item | Specification | Supplier and quote | Certificate or rating | Ordered |
|---|---|---|---|---|
| Gantry crane | portable, 500 kg class, adjustable height, trolley; span and height to fit the site record | TBC | rating plate, supplier load test | |
| Winch or fall-arrest block | rated for 35 kg dynamic load with shock allowance; controlled lowering | TBC | EN 360 or equivalent, to be checked | |
| Tether and shackles | rated, with a quick-release the operator can reach | TBC | rating marks | |
| E-stop pendant | red mushroom on yellow, two NC positive-opening contacts, latching, reset button | TBC | ISO 13850 device | |
| Safety relay module | Category 3 or better, monitored reset, PL d or e on the data sheet | TBC | data sheet with PL and MTTFD | |
| Contactors | two, rated for the rail current, mirror contacts | TBC | data sheet | |
| Bench supply | the kit's rail voltage, adjustable current limit, output switch, rated for the standing current with margin | TBC | | |

## Verification before use

The pre-session checks of WP-V-07 §4: rating labels confirmed, a static load test to twice the robot's mass on the
gantry, the E-stop functional test from the pendant, the supply's current limit set and recorded.

## Open items

| ID | Item | Owner | Due |
|---|---|---|---|
| OI-1 | Read the rail voltage and the standing current from the actuator data sheets and the harness; size the supply and the contactors | EM | before ordering |
| OI-2 | Enter the quotes and order (DQ-035 A) | PM | before the first hang test |
| OI-3 | File the certificates and data sheets under WP-H-07 | SM | with the acceptance record |
