import json
from pathlib import Path

import sc2
from sc2.constants import *


BARRACK_DISTANCE = 6
FACTORY_DISTANCE = 11
GHOST_DISTANCE = 5
SUPPLY_DISTANCE = 15

ATTACK_UNIT_TYPES = [UnitTypeId.GHOST, UnitTypeId.CYCLONE]

class CheeseBot(sc2.BotAI):
    with open(Path(__file__).parent / "../botinfo.json") as f:
        NAME = json.load(f)["name"]

    def __init__(self):
        self.STEPS = [
            [12, self.build_workers],
            [13, self.build_workers],
            [14, self.build_depot],
            [14, self.build_workers],
            [15, self.build_workers],
            [15, self.build_barracks],
            [15, self.build_refinery],
            [16, self.build_refinery],
            [16, self.build_workers],
            [17, self.build_workers],
            [18, self.build_workers],
            [20, self.build_barracks_tech_lab],
            [20, self.build_ghost_academy],
            [20, self.build_orbital_command],
            [19, self.build_depot],
            [19, self.build_ghost],
            [21, self.build_factory],
            [21, self.build_workers],
            [22, self.build_ghost],
            [24, self.build_workers],
            [24, self.build_depot],
            [26, self.build_workers],
            [26, self.build_factory_reactor],
            [26, self.build_depot],
            [27, self.build_cyclone],
            [27, self.build_cyclone],
            [28, self.attaaaaack],
            [19, self.build_ghost],
            [19, self.build_ghost],
            [28, self.build_cyclone],
            [28, self.build_cyclone],
            [28, self.attaaaaack],
            [19, self.build_ghost],
            [19, self.build_ghost],
            [28, self.build_cyclone],
            [1, self.build_cyclone],
            [1, self.attaaaaack],
            [19, self.build_ghost],
            [19, self.build_ghost],
            [1, self.build_cyclone],
            [1, self.build_cyclone],
            [1, self.attaaaaack],
            [19, self.build_ghost],
            [19, self.build_ghost],
            [1, self.build_cyclone],
            [1, self.build_cyclone],
            [1, self.attaaaaack],
            [19, self.build_ghost],
            [19, self.build_ghost],
            [1, self.build_cyclone],
            [1, self.build_cyclone],
            [1, self.attaaaaack],
            [19, self.build_ghost],
            [19, self.build_ghost],
            [1, self.build_cyclone],
            [1, self.build_cyclone],
            [1, self.attaaaaack],
            [19, self.build_ghost],
            [19, self.build_ghost],
            [1, self.build_cyclone],
            [1, self.build_cyclone],
            [1, self.attaaaaack],
            [19, self.build_ghost],
            [19, self.build_ghost],
            [1, self.build_cyclone],
            [1, self.build_cyclone],
            [1, self.attaaaaack],
            [19, self.build_ghost],
            [19, self.build_ghost],
            [1, self.build_cyclone],
            [1, self.build_cyclone],
            [1, self.attaaaaack],
            [19, self.build_ghost],
            [19, self.build_ghost],
            [1, self.build_cyclone],
            [1, self.build_cyclone],
            [1, self.attaaaaack],
            [19, self.build_ghost],
            [19, self.build_ghost],
            [1, self.build_cyclone],
            [1, self.build_cyclone],
            [1, self.attaaaaack],
            [19, self.build_ghost],
            [19, self.build_ghost],
            [1, self.build_cyclone],
            [1, self.build_cyclone],
            [1, self.attaaaaack],
            [19, self.build_ghost],
            [19, self.build_ghost],
            [1, self.build_cyclone],
            [1, self.build_cyclone],
            [1, self.attaaaaack],
            [19, self.build_ghost],
            [19, self.build_ghost],
            [1, self.build_cyclone],
            [1, self.build_cyclone],
            [1, self.attaaaaack],
            [19, self.build_ghost],
            [19, self.build_ghost],
            [1, self.build_cyclone],
            [1, self.build_cyclone],
            [1, self.attaaaaack],
            [19, self.build_ghost],
            [19, self.build_ghost],
            [1, self.build_cyclone],
            [1, self.build_cyclone],
            [1, self.attaaaaack],
            [19, self.build_ghost],
            [19, self.build_ghost],
            [1, self.build_cyclone],
            [1, self.build_cyclone],
            [1, self.attaaaaack],
            [19, self.build_ghost],
            [19, self.build_ghost],
            [1, self.build_cyclone],
            [1, self.build_cyclone],
            [1, self.attaaaaack],
            [19, self.build_ghost],
            [19, self.build_ghost],
            [1, self.build_cyclone],
            [1, self.build_cyclone],
            [1, self.attaaaaack],
            [19, self.build_ghost],
            [19, self.build_ghost],
            [1, self.build_cyclone],
            [1, self.build_cyclone],
            [1, self.attaaaaack],
            [999, self.build_depot]
        ]
        self.refineries = []
        self.is_attacking = False

    def get_command_center(self):
        cc = (self.units(UnitTypeId.COMMANDCENTER) | self.units(UnitTypeId.ORBITALCOMMAND))
        if cc.exists:
            return cc[0]
        else:
            return None

    async def build_refinery(self):
        cc = self.get_command_center()
        if self.can_afford(UnitTypeId.REFINERY):
            vgs = self.state.vespene_geyser.closer_than(20.0, cc)
            for vg in vgs:
                if self.units(UnitTypeId.REFINERY).closer_than(1.0, vg).exists:
                    break
                worker = self.select_build_worker(vg.position)
                if worker is None:
                    break
                if vg.tag in self.refineries:
                    break
                if vg.name != 'VespeneGeyser':
                    break
                self.refineries.append(vg.tag)
                return not await self.do(worker.build(UnitTypeId.REFINERY, vg))

    async def build_barracks_tech_lab(self):
        ready_raxes = self.units(UnitTypeId.BARRACKS).ready
        if ready_raxes.amount > 0 and self.can_afford(UnitTypeId.BARRACKSTECHLAB):
            return not await self.do(ready_raxes[0].train(UnitTypeId.BARRACKSTECHLAB))


    async def build_ghost_academy(self):
        cc = self.get_command_center()
        if self.can_afford(UnitTypeId.GHOSTACADEMY) and self.units(UnitTypeId.BARRACKSTECHLAB).ready.amount > 0:
            return not await self.build(UnitTypeId.GHOSTACADEMY, near=cc.position.towards(self.game_info.map_center, GHOST_DISTANCE))

    async def build_orbital_command(self):
        cc = self.get_command_center()
        if self.can_afford(UnitTypeId.ORBITALCOMMAND):
            return not await self.do(cc.train(UnitTypeId.ORBITALCOMMAND))

    async def build_ghost(self):
        barracks = self.units(UnitTypeId.BARRACKS)
        if barracks.exists and self.can_afford(UnitTypeId.GHOST) and self.units(UnitTypeId.GHOSTACADEMY).ready.amount > 0 and self.supply_left > 1:
            return not await self.do(barracks[0].train(UnitTypeId.GHOST))

    async def build_factory(self):
        cc = self.get_command_center()
        if self.can_afford(UnitTypeId.FACTORY) and self.units(UnitTypeId.BARRACKS).ready.amount > 0:
            return not await self.build(UnitTypeId.FACTORY, near=cc.position.towards(self.game_info.map_center, FACTORY_DISTANCE))

    async def build_factory_reactor(self):
        factories = self.units(UnitTypeId.FACTORY).ready
        if self.can_afford(UnitTypeId.FACTORYREACTOR) and factories.amount > 0:
            return not await self.do(factories[0].train(UnitTypeId.FACTORYREACTOR))

    async def build_cyclone(self):
        if self.can_afford(UnitTypeId.CYCLONE) and self.units(UnitTypeId.FACTORYREACTOR).ready.amount > 0 and self.supply_left > 2:
            return not await self.do(self.units(UnitTypeId.FACTORY)[0].train(UnitTypeId.CYCLONE))

    async def attaaaaack(self):
        if self.units(UnitTypeId.CYCLONE).ready.amount >= 2:
            self.is_attacking = True
            for unit_type in ATTACK_UNIT_TYPES:
                for unit in self.units(unit_type):
                    await self.do(unit.attack(self.enemy_start_locations[0]))
                for ghost in self.units(UnitTypeId.GHOST):
                    await self.do(ghost(AbilityId.BEHAVIOR_CLOAKON_GHOST))
            return True

    async def on_step(self, iteration):
        if iteration == 0:
            await self.chat_send(f"Name: {self.NAME}")
        cc = self.get_command_center()

        if not cc:
            target = self.enemy_start_locations[0]
            for unit in self.workers | self.units(UnitTypeId.GHOST) | self.units(UnitTypeId.CYCLONE):
                await self.do(unit.attack(target))
            return

        await self.gather_resources()
        if not self.is_attacking:
            await self.hold_troops()
        executed = await self.STEPS[0][1]()
        if executed:
            print("EXECUTED STEP {} {}".format(self.STEPS[0][0], self.STEPS[0][1].__name__))
            self.STEPS.pop(0)
            return executed

    async def build_depot(self):
        cc = self.get_command_center()
        if self.can_afford(UnitTypeId.SUPPLYDEPOT):
            return not await self.build(UnitTypeId.SUPPLYDEPOT, near=cc.position.random_on_distance(SUPPLY_DISTANCE))

    async def build_barracks(self):
        cc = self.get_command_center()
        if self.can_afford(UnitTypeId.BARRACKS) and self.units(UnitTypeId.SUPPLYDEPOT).ready.amount > 0:
            return not await self.build(UnitTypeId.BARRACKS, near=cc.position.towards(self.game_info.map_center, BARRACK_DISTANCE))

    async def build_workers(self):
        cc = self.get_command_center()
        if cc.is_ready and cc.noqueue:
            if self.can_afford(UnitTypeId.SCV) and self.supply_left > 0:
                print("Building worker, current count {}".format(self.workers.amount))
                return not await self.do(cc.train(UnitTypeId.SCV))

    async def gather_resources(self):
        for a in self.units(UnitTypeId.REFINERY):
            if a.assigned_harvesters < a.ideal_harvesters:
                w = self.workers.closer_than(20, a)
                if w.exists:
                    await self.do(w.random.gather(a))

        cc = self.get_command_center()
        for scv in self.units(UnitTypeId.SCV).idle:
            await self.do(scv.gather(self.state.mineral_field.closest_to(cc)))

    async def hold_troops(self):
        for unit in self.units(UnitTypeId.GHOST) | self.units(UnitTypeId.CYCLONE):
            await self.do(unit.hold_position())