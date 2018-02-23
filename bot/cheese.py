import json
from pathlib import Path

import sc2
from sc2.constants import *




class CheeseBot(sc2.BotAI):
    with open(Path(__file__).parent / "../botinfo.json") as f:
        NAME = json.load(f)["name"]



    def __init__(self):
        self.STEPS = [
            [14, self.build_depot],
            [15, self.build_barracks],
            [15, self.build_refinery],
            [16, self.build_refinery],
            [20, self.build_barracks_tech_lab],
            [20, self.build_ghost_academy],
            [20, self.build_orbital_command],
            [20, self.build_depot],
            [20, self.build_ghost],
            [20, self.build_factory],
            [20, self.build_ghost],
            [24, self.build_depot],
            [26, self.build_factory_reactor],
            [26, self.build_depot],
            [27, self.build_cyclone],
            [27, self.build_cyclone],
            [27, self.attaaaaack],
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
                await self.do(worker.build(UnitTypeId.REFINERY, vg))
                return True


    async def build_barracks_tech_lab(self):
        ready_raxes = self.units(UnitTypeId.BARRACKS).ready
        if ready_raxes.amount > 0 and self.can_afford(UnitTypeId.BARRACKSTECHLAB):
            await self.do(ready_raxes[0].train(UnitTypeId.BARRACKSTECHLAB))
            return True


    async def build_ghost_academy(self):
        cc = self.get_command_center()
        if self.can_afford(UnitTypeId.GHOSTACADEMY) and self.units(UnitTypeId.BARRACKS).ready.amount > 0:
            await self.build(UnitTypeId.GHOSTACADEMY, near=cc.position.random_on_distance(5))
            return True

    async def build_orbital_command(self):
        cc = self.get_command_center()
        if self.can_afford(UnitTypeId.ORBITALCOMMAND):
            await self.do(cc.train(UnitTypeId.ORBITALCOMMAND))
            return True

    async def build_ghost(self):
        barracks = self.units(UnitTypeId.BARRACKS)[0]
        if self.can_afford(UnitTypeId.GHOST) and self.units(UnitTypeId.GHOSTACADEMY).ready.amount > 0 and self.supply_left > 2:
            await self.do(barracks.train(UnitTypeId.GHOST))
            return True

    async def build_factory(self):
        cc = self.get_command_center()
        if self.can_afford(UnitTypeId.FACTORY) and self.units(UnitTypeId.BARRACKS).ready.amount > 0:
            await self.build(UnitTypeId.FACTORY, near=cc.position.towards(self.game_info.map_center, 9))
            return True

    async def build_factory_reactor(self):
        factories = self.units(UnitTypeId.FACTORY).ready
        if self.can_afford(UnitTypeId.FACTORYREACTOR) and factories.amount > 0:
            await self.do(factories[0].train(UnitTypeId.FACTORYREACTOR))
            return True

    async def build_cyclone(self):
        if self.can_afford(UnitTypeId.CYCLONE) and self.units(UnitTypeId.FACTORYREACTOR).ready.amount > 0 and self.supply_left > 3:
            foo = await self.do(self.units(UnitTypeId.FACTORY)[0].train(UnitTypeId.CYCLONE))
            print("**** foo")
            print(foo)
            return True

    async def attaaaaack(self):
        if (self.units(UnitTypeId.CYCLONE).ready.amount == 2):
            for unit in self.units(UnitTypeId.GHOST):
                await self.do(unit(AbilityId.BEHAVIOR_CLOAKON_GHOST))
            self.is_attacking = True
            #for unit in self.workers | self.units(UnitTypeId.GHOST) | self.units(UnitTypeId.CYCLONE):
            #    await self.do(unit.attack(self.enemy_start_locations[0]))
            return True

    async def on_step(self, iteration):
        if iteration == 0:
            await self.chat_send(f"Name: {self.NAME}")
        cc = self.get_command_center()

        if not cc or self.is_attacking:
            target = self.known_enemy_structures.random_or(self.enemy_start_locations[0]).position
            for unit in self.workers | self.units(UnitTypeId.GHOST) | self.units(UnitTypeId.CYCLONE):
                await self.do(unit.attack(target))
            return
            # visible_enemy_units = self.known_enemy_units.filter(lambda unit: unit.is_visible and not unit.is_flying)
            # if visible_enemy_units.amount > 0:
            #     for unit in self.units(UnitTypeId.GHOST):
            #         if not unit.cloak:
            #             await self.do(unit(AbilityId.BEHAVIOR_CLOAKON_GHOST))
            # race_workers = [UnitTypeId.PROBE, UnitTypeId.SCV, UnitTypeId.DRONE]
            # workers = visible_enemy_units.filter(lambda unit: unit.type_id in race_workers)
            # not_workers = visible_enemy_units.filter(lambda unit: unit.type_id not in race_workers)
            # target = not_workers.random_or(workers.random_or(self.known_enemy_structures.random_or(self.enemy_start_locations[0])))
            # for unit in self.workers | self.units(UnitTypeId.GHOST) | self.units(UnitTypeId.CYCLONE):
            #     await self.do(unit.attack(self.enemy_start_locations[0]))
            # return

        await self.gather_resources()
        await self.hold_troops()

        worker_count = self.workers.amount
        next_step_count = self.STEPS[0][0]
        if worker_count >= next_step_count:
            executed = await self.STEPS[0][1]()
            if executed:
                print("EXECUTED STEP {} {}".format(next_step_count, self.STEPS[0][1].__name__))
                self.STEPS.pop(0)
                return executed
        else:
            await self.build_workers()

    async def build_depot(self):
        cc = self.get_command_center()
        if self.can_afford(UnitTypeId.SUPPLYDEPOT):
            await self.build(UnitTypeId.SUPPLYDEPOT, near=cc.position.random_on_distance(3))
            return True

    async def build_barracks(self):
        cc = self.get_command_center()
        if self.can_afford(UnitTypeId.BARRACKS) and self.units(UnitTypeId.SUPPLYDEPOT).ready.amount > 0:
            await self.build(UnitTypeId.BARRACKS, near=cc.position.towards(self.game_info.map_center, 6))
            return True

    async def build_workers(self):
        cc = self.get_command_center()
        if cc.is_ready and cc.noqueue:
            if self.can_afford(UnitTypeId.SCV):
                print("Building worker, current count {}".format(self.workers.amount))
                await self.do(cc.train(UnitTypeId.SCV))
                return True

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